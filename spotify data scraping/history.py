import ast
import os
import requests
from datetime import datetime
from typing import List
import spotipy
import spotipy.util as util
from os import listdir
import pandas as pd

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
    track_ids = []
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
                'Authorization': f'Bearer ' + token,
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
                    if track_id:
                       track_ids.append(track_id)
                
        except Exception as e:
               print(f"Error in batch {batch_number + 1}: {e}")
    return track_ids
   
    
    
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
       
def get_saved_ids(tracks, path: str = 'spotify data scraping/output/track_ids.csv') -> dict:
   
    track_ids = {track: None for track in tracks}
    #folder, filename = path.split('/')
    #path = os.path.join(folder, filename)
    folder = 'spotify data scraping/output/'
    filename = 'track_ids.csv'
    print(path)
    if filename in os.listdir(folder):
        try:
            idd_dataframe = pd.read_csv('spotify data scraping/output/track_ids.csv', 
                                     names = ['name', 'idd'])
            idd_dataframe = idd_dataframe[1:]                    #removing first row
            added_tracks = 0
            for index, row in idd_dataframe.iterrows():
                if not row[1] == 'nan':                          #if the id is not nan
                    track_ids[row[0]] = row[1]                    #add the id to the dict
                    added_tracks += 1
            print(f'Saved IDs successfully recovered for {added_tracks} tracks.')
        except:
            print('Error. Failed to recover saved IDs!')
            pass
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