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

#streamingPath = 'D:/Code_Repositories_Mohit/mohit_github_repos/my-music-analysis-main/spotify data scraping/my streaming data'
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

def get_api_id(track_name: str, token: str, 
                artist: str = None) -> str:
    
    '''Performs a query on Spotify API to get a track ID.
    See https://curl.trillworks.com/'''
   
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + token,
    }
    
    params = [
    ('q', track_name),
    ('type', 'track'),
    ]
    
    if artist: 
        params.append(('artist', artist))
        
    try:
        response = requests.get('https://api.spotify.com/v1/search', 
                    headers = headers, params = params, timeout = 5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None
track_csv_path = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/track_ids.csv'    
def get_saved_ids(tracks, path: str = track_csv_path) -> dict:
    import os
    print(os.getcwd())
    track_ids = {track: None for track in tracks}
    #folder, filename = path.split('/')
    #path = os.path.join(folder, filename)
    folder = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/'
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
feature_path = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/features.csv'   
def get_saved_features(tracks, path = feature_path):
    #folder, file = path.split('/')
    folder = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/'
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