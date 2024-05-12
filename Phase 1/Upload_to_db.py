import pandas as pd
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fma_database"]
collection = db["Songs_collection"]

# Load the CSV file containing tracks with features
tracks_df = pd.read_csv('merged_tracks_with_features.csv')

# Convert DataFrame to a list of dictionaries (one for each track)
tracks_data = tracks_df.to_dict(orient='records')

# Insert each track as a separate document into the MongoDB collection
collection.insert_many(tracks_data)

print("CSV data uploaded to MongoDB successfully.")

