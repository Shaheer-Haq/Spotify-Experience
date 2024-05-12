## Spotify-Experience
# Introduction

Welcome music lovers, to your gateway to the world of endless melodies, rhythms, and harmonies - the Ultimate Spotify Web App! Dive into a musical adventure like no other, where every beat, every lyric, and every note awaits your discovery.

# Files (Phase 1)
# 1. Feature_Extraction.py

This script is designed to merge two CSV files containing tracks details and features respectively using the Pandas library in Python.

## Files Included
1. merge_tracks.py: Python script for merging tracks details and features.
2. tracks_with_genre_titles.csv: CSV file containing track details including track ID and genre titles.
3.features.csv: CSV file containing features of tracks.
4. merged_tracks.csv: Output CSV file after merging tracks details and features.

## Requirements
1. Python 3.x
2. Pandas library (pip install pandas)

## Usage

Place tracks_with_genre_titles.csv and features.csv in the same directory as merge_tracks.py.
Run the script merge_tracks.py.
The merged output will be saved as merged_tracks.csv in the same directory.

## Process
1. Loading DataFrames: The script loads two CSV files, one containing track details and another containing features, into Pandas DataFrames.
2. Handling Non-Integer Track IDs: Checks for non-integer values in the track ID column of the track details DataFrame. If found, it displays them and handles them accordingly (e.g., removing rows).
3. Data Type Conversion: Converts the track ID column in both DataFrames to int64 data type to ensure consistency.
4. Merging DataFrames: Merges the two DataFrames on the track ID column using an inner join.
5. Saving Merged DataFrame: Saves the merged DataFrame as merged_tracks.csv without including the index.

## Output
merged_tracks.csv: Contains the merged data of track details and features.

# 2. Upload_to_db.py

## Overview
This Python script facilitates the upload of CSV data into a MongoDB database. It converts the CSV file into a list of dictionaries and inserts each dictionary (representing a track) as a separate document into a MongoDB collection.

## Requirements
1. Python 3.x
2. Pandas library (pip install pandas)
3. PyMongo library (pip install pymongo)
4. MongoDB server running locally or accessible via network

## Usage
1. Ensure that MongoDB server is running locally or accessible via network.
2. Place the CSV file containing tracks data (merged_tracks_with_features.csv) in the same directory as the script.
3. Run the script csv_to_mongodb_uploader.py.
4. CSV data will be uploaded to the specified MongoDB database and collection.

## Configuration
1. MongoDB Connection: Modify the MongoDB connection string in the script ("mongodb://localhost:27017/") to match your MongoDB server configuration.
2. Database and Collection: Adjust the database name ("fma_database") and collection name ("Songs_collection") as needed in the script.

## Input
merged_tracks_with_features.csv: CSV file containing tracks data including features.

## Output
Uploaded data will be stored in the specified MongoDB collection.

# Files (Phase 2)
# 1. model_training.py

## Overview
This PySpark script implements a music recommendation system using linear regression for predicting user ratings based on various features of tracks. Additionally, it recommends top tracks within a specified genre based on listens.

## Requirements
1. Apache Spark (with PySpark)
2. PyMongo (for MongoDB integration)
3. MongoDB server running locally or accessible via network

## Usage
1. Install Apache Spark and PyMongo.
2. Ensure MongoDB server is running locally or accessible via network.
3. Place the script (music_recommendation.py) in your PySpark environment.
4. Run the script using spark-submit music_recommendation.py.

## Features
1. Linear Regression Model: Builds a linear regression model to predict user ratings based on track features.
2. Feature Engineering: Includes handling string columns, converting them to numerical or categorical types, and creating a features column.
3. Model Evaluation: Evaluates the model's performance using RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error).
4. Recommendation System: Recommends top tracks within a specified genre based on listens.
Configuration
5. MongoDB Connection: Modify the MongoDB connection string in the script ("mongodb://localhost:27017/") to match your MongoDB server configuration.
6. Genres and Labels: Adjust the genre for recommendation (genre_to_recommend) and label for regression (label) as needed in the script.

## Input
MongoDB Collection: Data is loaded from the specified MongoDB collection (Songs_collection) into a Spark DataFrame.

## Output
1. Model Performance: RMSE and MAE are printed to evaluate the model's performance.
2. Recommended Tracks: Top tracks within the specified genre are recommended and their details are displayed.

# Files (Phase 3)
# 1. app.py

## Overview
This Flask web application provides music recommendations based on genre preferences using a PySpark-based recommendation model trained on data stored in MongoDB. It allows users to select a genre and receive recommendations for top tracks within that genre.

## Requirements
1. Python 3.x
2. Flask
3. PySpark (with Spark installed)
4. PyMongo (for MongoDB integration)
5. MongoDB server running locally or accessible via network

## Usage
1. Install Python, Flask, PySpark, and PyMongo.
2. Ensure MongoDB server is running locally or accessible via network.
3. Place the script (app.py) in your project directory.
4. Create HTML templates (index.html, spotify.html, genres.html, search.html, login.html, signup.html, recommendations.html) for different pages.
5. Run the Flask app using python app.py.
6. Access the web app in your browser at http://localhost:5000.

## Features
1. Music Recommendations: Provides recommendations for top tracks within a specified genre.
2. Interactive Interface: Offers a user-friendly interface for selecting genres and viewing recommendations.
3. Backend Spark Integration: Uses PySpark for feature engineering and training a recommendation model.
4. MongoDB Integration: Loads data from MongoDB into Spark DataFrame for model training and recommendation generation.

## Configuration
1. MongoDB Connection: Modify the MongoDB connection string in the script ("mongodb://localhost:27017/") to match your MongoDB server configuration.

## Project Structure
1. Templates: Contains HTML templates for different pages of the web app.
2. Static: Contains static files (e.g., CSS, JavaScript) for styling and functionality.


# Contributors
21i-1657 Shaheer-E-Haq,
21i-1694 Moeez Ahmed,
21i-1743 Meeran Ali

# Issues
If you encounter any issues or have suggestions for improvement, please feel free to raise an issue or submit a pull request.
