import pandas as pd

# Load tracks details CSV file
tracks_details_df = pd.read_csv('tracks_with_genre_titles.csv')

# Load features CSV file and skip the first three rows
features_df = pd.read_csv('features.csv', skiprows=3)

# Check for non-integer values in the track_id column of tracks_details_df
non_integer_track_ids = tracks_details_df[~tracks_details_df['track_id'].astype(str).str.isdigit()]['track_id']

# If there are non-integer track IDs, display them and handle them accordingly
if not non_integer_track_ids.empty:
    print("Non-integer track IDs found in the tracks_details_df DataFrame:")
    print(non_integer_track_ids)
    # Handle non-integer track IDs (e.g., remove rows, convert them to NaN, etc.)
    # For example, you can drop rows with non-integer track IDs:
    tracks_details_df = tracks_details_df[tracks_details_df['track_id'].astype(str).str.isdigit()]

# Convert track_id column to int64 data type in both DataFrames
tracks_details_df['track_id'] = tracks_details_df['track_id'].astype('int64')
features_df['track_id'] = features_df['track_id'].astype('int64')

# Merge both dataframes on the track ID column
merged_df = pd.merge(tracks_details_df, features_df, on='track_id', how='inner')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged_tracks.csv', index=False)

print("Merged CSV file saved successfully.")

