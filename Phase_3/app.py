from flask import Flask, render_template, request
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id, desc, sum
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import IntegerType, StringType
from pyspark.ml.feature import StringIndexer, VectorAssembler
import pymongo

# Create a Flask app
app = Flask(__name__)

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

@app.route('/train_model')
def train_model():
    global model, training_data

    # Feature Engineering
    data = data.withColumn("user_id", monotonically_increasing_id())
    data = data.withColumn("rating", col("listens").cast(IntegerType()))
    indexer1 = StringIndexer(inputCol="genre_titles", outputCol="genre_index")
    indexer2 = StringIndexer(inputCol="artist_name", outputCol="artist_index")
    data = indexer1.fit(data).transform(data)
    data = indexer2.fit(data).transform(data)
    data = data.dropna()
    assembler = VectorAssembler(inputCols=["user_id", "track_id", "genre_index", "artist_index"], outputCol="features_vec")
    data = assembler.transform(data)

    # Split the data into training and test sets
    (training, _) = data.randomSplit([0.8, 0.2])
    training_data = training

    # Define label
    label = "rating"

    # Create linear regression model
    lr = LinearRegression(featuresCol="features_vec", labelCol=label, regParam=0.1)

    # Fit the model
    model = lr.fit(training)

    # Return a success message
    return "Model trained successfully"

def make_recommendations(genre_to_recommend):
    # Recommend tracks for the given genre
    top_tracks_in_genre = data.filter(data.genre_titles == genre_to_recommend) \
        .groupBy("track_id") \
        .agg(sum("listens").alias("total_listens")) \
        .orderBy(desc("total_listens")) \
        .limit(20) \
        .select("track_id")

    top_tracks_details = top_tracks_in_genre.join(data, "track_id", "inner").select(
        "track_id", "track_title", "artist_name", "genre_titles", "listens"
    )

    recommendations = top_tracks_details.collect()

    return recommendations
   

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/spotify.html')
def spotify():
    return render_template('spotify.html')
    
@app.route('/genres.html')
def genres():
    return render_template('genres.html')
    
@app.route('/search.html')
def search():
    return render_template('search.html')    
    
@app.route('/login.html')
def login():
    return render_template('login.html')   
    
@app.route('/signup.html')
def signup():
    return render_template('signup.html')   
    

@app.route('/recommendations.html', methods=['POST'])
def get_recommendations():
    selected_genre = request.form['genre']
    recommendations = make_recommendations(selected_genre)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)

