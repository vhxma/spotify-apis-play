import spotipy #spotipy = lightweight Python library for the Spotify Web API
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd
from tqdm import tqdm

load_dotenv()

cli_id = os.environ['CLI_ID']
cli_secret = os.environ['CLI_SECRET']
person_dict = {'ranupi': 'Mikaela','gilesknight': 'Giles','Vanessa': 'Vanessa'}

# Authentication without user
client_credentials_manager = SpotifyClientCredentials(client_id=cli_id, client_secret=cli_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Get playlist (must be public)
playlist_link = "https://open.spotify.com/playlist/7GBImxgFe4ga5qqWzMnbkQ"


#get track info with song name, artist, popularity of song, tempo, danceability and who added
#requires name of playlist, and a person dict to identify user by name
def get_track_info(playlist_link, person_dict, sp):
    track_info = pd.DataFrame(columns=['track_name', 'artist', 'track_pop', 'tempo', 'danceability', 'user'])

    for track in tqdm(sp.playlist_tracks(playlist_link)["items"], desc='Adding tracks...'):
        #URI
        track_uri = track["track"]["uri"]
        
        #Track name
        track_name = track["track"]["name"]
        #print(track_name)
        
        #Name, popularity, genre
        artist_name = track["track"]["artists"][0]["name"]
        #print(artist_name)
        
        #Popularity of the track
        track_pop = track["track"]["popularity"]
        #print(f'Popularity: {track_pop}') #higher the score, the more popular

        #get danceability
        features = sp.audio_features(track_uri)[0]
        tempo = features['tempo']
        #print(f'Tempo: {tempo}')
        danceability = features['danceability']
        #print(f'Danceability: {danceability}')

        #get display name of who added the song
        person = sp.user(track['added_by']['id'])
        person_name = person['display_name']
        #print(f'Added by: {person_dict[person_name]}')

        info_row = pd.Series({
            'track_name': track_name,
            'artist': artist_name,
            'track_pop': track_pop,
            'tempo': tempo,
            'danceability': danceability,
            'user': person_dict[person_name]
        })

        track_info = pd.concat([track_info, info_row.to_frame().T], ignore_index=True)
        
        #print('\n')

    #print(track_info)
    return track_info

track_info = get_track_info(playlist_link, person_dict, sp)

#once we have the track info and want to save them as csvs
# track_info.to_csv('data/track_info.csv')
# track_info['track_name'].to_csv('data/tracks.csv')

# track_info = pd.read_csv('data/track_info.csv').drop('Unnamed: 0', axis=1)
# print(track_info)
# tracks = pd.read_csv('data/tracks.csv').drop('Unnamed: 0', axis=1)
# print(tracks.head())