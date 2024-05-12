from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id, desc, sum
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import IntegerType, StringType
from pyspark.ml.feature import StringIndexer, VectorAssembler
import pymongo

# Create a Spark session
spark = SparkSession.builder \
    .appName("MusicRecommendation") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fma_database"]
collection = db["Songs_collection"]

# Load data from MongoDB into Spark DataFrame
data = spark.createDataFrame(collection.find())

# Feature Engineering: Adding more features if available
data = data.withColumn("user_id", monotonically_increasing_id())
data = data.withColumn("rating", col("listens").cast(IntegerType()))

# Handle string columns: Convert them to numerical or categorical types
indexer1 = StringIndexer(inputCol="genre_titles", outputCol="genre_index")
indexer2 = StringIndexer(inputCol="artist_name", outputCol="artist_index")
data = indexer1.fit(data).transform(data)
data = indexer2.fit(data).transform(data)

# Drop rows with missing values
data = data.dropna()

# Create a features column
assembler = VectorAssembler(inputCols=["user_id", "track_id", "genre_index", "artist_index"], outputCol="features_vec")
data = assembler.transform(data)

# Split the data into training and test sets
(training, test) = data.randomSplit([0.8, 0.2])

# Define label
label = "rating"

# Create linear regression model
lr = LinearRegression(featuresCol="features_vec", labelCol=label, regParam=0.1)

# Fit the model
model = lr.fit(training)

# Evaluate the model
predictions = model.transform(test)

# Calculate RMSE
evaluator_rmse = RegressionEvaluator(metricName="rmse", labelCol=label, predictionCol="prediction")
rmse = evaluator_rmse.evaluate(predictions)
print("Root Mean Squared Error (RMSE) = {:.2f}".format(rmse))

# Calculate MAE
evaluator_mae = RegressionEvaluator(metricName="mae", labelCol=label, predictionCol="prediction")
mae = evaluator_mae.evaluate(predictions)
print("Mean Absolute Error (MAE) = {:.2f}".format(mae))

# Recommend 5 tracks with the highest listens in a particular genre
genre_to_recommend = "Rock"  # Change to the desired genre
top_tracks_in_genre = data.filter(data.genre_titles == genre_to_recommend) \
    .groupBy("track_id") \
    .agg(sum("listens").alias("total_listens")) \
    .orderBy(desc("total_listens")) \
    .limit(5) \
    .select("track_id")

top_tracks_in_genre.show()

# Join data with top_tracks_in_genre DataFrame on track_id column
top_tracks_details = top_tracks_in_genre.join(data, "track_id", "inner").select(
    "track_id", "track_title", "artist_name", "genre_titles", "listens"
)

# Show the top tracks details
top_tracks_details.show()


# Stop the Spark session
spark.stop()

