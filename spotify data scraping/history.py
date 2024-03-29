import ast
import os
import requests
from datetime import datetime
from typing import List
import spotipy
import spotipy.util as util
from os import listdir
import pandas as pd
import csv

def get_token(user: str, 
              client_id: str,
              client_secret: str,
              redirect_uri: str,
              scope: str) -> str:
  
    token = util.prompt_for_user_token(user,scope,
                                               client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri)
    return token


def get_streamings(path: str = 'spotify data scraping/my streaming data/'
                ) -> List[dict]:
    
    '''Returns a list of streamings form spotify MyData dump.
    Will not acquire track features.'''
    
    files = [path + x for x in listdir(path) if x.startswith('StreamingHistory')]
    
    all_streamings = []
    
    for file in files: 
        with open(file, 'r', encoding='UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming in new_streamings]
            
    #adding datetime field
    for streaming in all_streamings:
        streaming['datetime'] = datetime.strptime(streaming['endTime'], '%Y-%m-%d %H:%M')    
    return all_streamings


import requests

"""def get_api_id(track_names: list, token: str, artist: str = None) -> dict:
    '''Performs a batch query on Spotify API to get track IDs.
    See https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-several-tracks'''
    batch_size = 50
    total_tracks = len(track_names) 

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer ' + token,
    }

    # Calculate the number of batches needed
    num_batches = (total_tracks + batch_size - 1) // batch_size

    # Iterate through batches
    for batch_number in range(num_batches):
        # Calculate start and end indices for the current batch
        start_index = batch_number * batch_size
        end_index = min((batch_number + 1) * batch_size, total_tracks)
        print("inside batch tracks")
        # Extract batch of tracks
        batch_tracks = track_names[start_index:end_index]
        print("inside batch tracks")
        # Prepare batch request parameters
        params = {"ids": ",".join(batch_tracks)}
        
        try:
             # Send batch request to the API
            response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
            json = response.json()
            track_ids = {}
            for track_info in json.get('tracks', []):
                track_ids[track_info['name']] = track_info['id']
            return track_ids

            # Check if the request was successful
            if response.status_code == 200:
               # Process the response (replace with actual processing logic)
               print(f"Batch {batch_number + 1}/{num_batches} - Response: {response.json()}")
            else:
               # Handle errors (replace with actual error handling logic)
               print(f"Batch {batch_number + 1}/{num_batches} - Error: {response.status_code}")
        
        except Exception as e:
         print(f"Error: {e}")
        return {}
        """

def get_api_id(track_name: str, token: str, 
                artist: str = None) -> str:
    
    '''Performs a query on Spotify API to get a track ID.
    See https://curl.trillworks.com/'''

    batch_size = 50
    total_tracks = len(track_name)
    track_names_list = list(track_name)
    track_id_dictionary = {}
    # Calculate the number of batches needed
    num_batches = (total_tracks + batch_size - 1) // batch_size

    for batch_number in range(num_batches):
        # Calculate start and end indices for the current batch
        start_index = batch_number * batch_size
        end_index = min((batch_number + 1) * batch_size, total_tracks)
        print("inside batch tracks")
        # Extract batch of tracks
        batch_tracks = track_names_list[start_index:end_index]
        print("inside batch tracks")
        # Prepare batch request parameters
        params = {"ids": ",".join(batch_tracks)}
        
        try:
                headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer ' + token ,
                }
                
                params = [
                ('q', batch_tracks
                 ),
                ('type', 'track'),
                ('limit', '50'),
                ('offset', '0')
                ]
             # Send batch request to the API
                response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
                json = response.json()
                
                for track_info in json.get('tracks', {}).get('items', []):
                    track_id = track_info.get('id')
                    track_name =  track_info.get('name')
                      # Check if track name already exists in the dictionary
                    if track_name in track_id_dictionary:
                       # If the track name exists, append the track ID to the existing list
                       track_id_dictionary[track_name].append(track_id)
                    else:
                       # If the track name does not exist, create a new list with the track ID
                       track_id_dictionary[track_name] = [track_id]
                
        except Exception as e:
               print(f"Error in batch {batch_number + 1}: {e}")
    return track_id_dictionary
   
    
    
# Example usage:
# track_names_list = ["track1", "track2", "track3"]
# token = "your_spotify_api_token"
# result = get_api_id(track_names_list, token)
# print(result)


# Example usage:
# track_names_list = ["track1", "track2", "track3"]
# token = "your_spotify_api_token"
# result = get_api_id(track_names_list, token)
# print(result)

    

#track_csv_path = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/track_ids.csv' 
       
def get_saved_ids(tracks):
  """
  Reads track names and IDs from a CSV file where the first column is blank
  and track IDs span across multiple columns (unknown number).
  Returns a dictionary mapping track names to lists of track IDs.
  """
  total_track_ids = 0
  track_ids = {}
  with open('spotify data scraping/output/track_ids.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    # Skip the blank first column
    next(reader)

    for row in reader:
      track_name = row[0]
      track_ids_list = []  # Store all track IDs for this song

      # Iterate through all columns starting from the second (track name)
      for col_index in range(1, len(row)):
        track_id = row[col_index]
        if track_id:  # Check if value is not empty
          track_ids_list.append(track_id)
          total_track_ids += 1

      # Store the list of track IDs for the song
      track_ids.setdefault(track_name, []).extend(track_ids_list)
  print("Total Track IDs:", total_track_ids)
  return track_ids








          
    
def get_api_features(track_id: str, token: str) -> dict:
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None
    
#feature_path = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/features.csv'   
    
def get_saved_features(tracks, path = 'spotify data scraping/output/features.csv'):
    #folder, file = path.split('/')
    folder = 'spotify data scraping/output/'
    file = 'features.csv' 
    track_features = {track: None for track in tracks}
    if file in listdir(folder):
        features_df = pd.read_csv(path, index_col = 0)
        n_recovered_tracks = 0
        for track in features_df.index:
            features = features_df.loc[track, :]
            if not features.isna().sum():          #if all the features are there
                track_features[track] = dict(features)
                n_recovered_tracks += 1
        print(f"Added features for {n_recovered_tracks} tracks.")
        return track_features
    else:
        print("Did not find features file.")
        return track_features