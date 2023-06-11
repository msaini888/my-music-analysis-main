# -*- coding: utf-8 -*-
"""
author = 'Vincy Hu'

"""

#import packages
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd

client_id = '575003a724fb4f64bebd10949606f9e5'
client_secret = '9f70d62278184dbc929af2c840ad7195'
username = 'a07wqhmlqmvs0lfjbckmgiizu'

# create a dataframe to store infomation of my playlists 
my_playlist =  pd.DataFrame(columns=["id", "spotify_id", "list_name"])

# getting playlist info from spotify
client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlists = sp.user_playlists(username) # input your spotify account id here

# converting spotify data into dataframe
while playlists:
    for i, playlist in enumerate(playlists['items']): 
        spotifyid = playlist['id'] 
        listname = playlist['name'] 
        my_playlist.loc[len(my_playlist)] = {'id': i+1,
                                     'spotify_id': spotifyid,
                                     'list_name': listname}
        
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

# dataframe for song
my_song =  pd.DataFrame(columns=["list_id", "song_id","song_name","artist","popularity",'release_date']
                       )

# getting song info from each playlist
for listid in my_playlist["spotify_id"]:
    songs = []
    content = sp.user_playlist_tracks(username, listid, fields=None, limit=100, offset=0, market=None)
    songs += content['items']
    for song in songs:
     new_row = {"list_id": listid,
               "song_id": song['track']['id'],
               "song_name": song['track']['name'],
               "artist": song['track']['artists'][0]['name'],
               "popularity": song['track']['popularity'],
               "release_date": song['track']['album']['release_date']}
     my_song.loc[len(my_song)] = new_row

# song feature dataframe
my_feature = pd.DataFrame(columns=["song_id","energy", "liveness","tempo","speechiness",
                                "acousticness","instrumentalness","danceability",
                                "duration_ms","loudness","valence",
                                "mode","key"])
# playlist songs' features
for song in my_song['song_id']:
    features = sp.audio_features(tracks=[song])[0]
    new_row = {"song_id": song,
               "energy": features['energy'],
               "liveness": features['liveness'],
               "tempo": features['tempo'],
               "speechiness": features['speechiness'],
               "acousticness": features['acousticness'],
               "instrumentalness": features['instrumentalness'],
               "danceability": features['danceability'],
               "duration_ms": features['duration_ms'],
               "loudness": features['loudness'],
               "valence": features['valence'],
               "mode": features['mode'],
               "key": features['key']}
    my_feature.loc[len(my_feature)] = new_row

# merging the song info and song features dataframe
song_feature = pd.merge(my_song,my_feature,how='left',left_on='song_id', right_on='song_id')
list_song_feature = pd.merge(my_playlist,song_feature,how='left',left_on='spotify_id', right_on='list_id')

# exporting to csv file
list_song_feature.to_csv('playlist.csv')