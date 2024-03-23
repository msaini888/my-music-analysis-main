'''

author = 'Vlad Gheorghe'


'''
import history
import pandas as pd
from time import sleep
from config import *

def main():

    #recover streamings history
    token = history.get_token(username, client_id, 
                              client_secret, redirect_uri, scope)
    
    streamings = history.get_streamings()
    print(f'Recovered {len(streamings)} streamings.')
    
    #getting a list of unique tracks in our history
    tracks = set([streaming['trackName'] for streaming in streamings])
    print(tracks)
    print(f'Discovered {len(tracks)} unique tracks.')
    
    #getting saved ids for tracks
    track_ids = history.get_saved_ids(tracks)
    print(type(track_ids))
    print(track_ids.items())
    #checking tracks that still miss idd
    #tracks_missing_idd = len([track for track in tracks if track_ids.get(track) is None])
    #track_names_to_query = [track for track, idd in track_ids.items() if idd is None]
    # Initialize a set to store the song names with missing track IDs
    tracks_missing_id = set(track_ids.keys())
    print(f'There are {len(tracks_missing_id)} tracks missing ID.')

    if (tracks_missing_id):
        try:
            track_id_dictionary = history.get_api_id(list(tracks_missing_id), token)
            track_ids = track_id_dictionary
            # Initialize an empty set to store unique track IDs
            unique_track_ids = set()

            # Iterate over the values (lists of track IDs) in the track_id_dictionary
            for track_ids_list in track_id_dictionary.values():
               # Add each track ID from the list to the set
                unique_track_ids.update(track_ids_list)

                # Now unique_track_ids contains all the unique track IDs
                # Get the count of unique track IDs
            unique_track_count = len(unique_track_ids)
            print("Total unique track IDs:", unique_track_count)
                    
            # for song_name, track_id in track_id_dictionary.items():
            #     if track_ids.get(song_name) is None:
            #         track_ids[song_name] = track_id

            #         # Update the set of tracks with missing IDs
            # tracks_missing_id = {song_name for song_name, track_id in track_ids.items() if track_id is None}
                    
            print("Total IDs found:", len(track_id_dictionary))
                    
        except Exception as e:
            print(f"Error: {e}")

    ids_path = 'spotify data scraping/output/track_ids.csv'
    ids_dataframe = pd.DataFrame.from_dict(track_ids, orient = 'index')
    ids_dataframe.to_csv(ids_path)
    #recovering saved features
    track_features = history.get_saved_features(tracks)
    tracks_without_features = [track for track in tracks if track_features.get(track) is None]
    print(f"There are still {len(tracks_without_features)} tracks without features.")
    path = 'C:/Users/Admin/Downloads/my-music-analysis-main/my-music-analysis-main/spotify data scraping/output/features.csv'
    
    #connecting to spotify API to retrieve missing features
    if len (tracks_without_features):
        print('Connecting to Spotify to extract features...')
        acquired = 0
        for track, idd in track_ids.items(): 
            if idd is not None and track in tracks_without_features:
                try:
                    features = history.get_api_features(idd, token)
                    track_features[track] = features
                    if features:
                        acquired += 1
                        print(f'Acquired features: {track}. Total: {acquired}')
                except:
                    features = None
        tracks_without_features = [track for track in tracks if track_features.get(track) is None]
        print(f'Successfully recovered features of {acquired} tracks.')
        if len(tracks_without_features):
            print(f'Failed to identify {len(tracks_without_features)} items. Some of these may not be tracks.')
        
        #saving features 
        features_dataframe = pd.DataFrame(track_features).T
        features_dataframe.to_csv(path)
        print(f'Saved features to {path}.')
    
    #joining features and streamings
    print('Adding features to streamings...')
    streamings_with_features = []
    for streaming in streamings:
        track = streaming['trackName']
        features = track_features[track]
        if features:
            streamings_with_features.append({'name': track, **streaming, **features})
    print(f'Added features to {len(streamings_with_features)} streamings.')
    print('Saving streamings...')
    df_final = pd.DataFrame(streamings_with_features)
    df_final.to_csv('spotify data scraping/output/final.csv')
    perc_featured = round(len(streamings_with_features) / len(streamings) *100, 2)
    print(f"Done! Percentage of streamings with features: {perc_featured}%.") 
    print("Run the script again to try getting more information from Spotify.")
    
if __name__ == '__main__':
    main()