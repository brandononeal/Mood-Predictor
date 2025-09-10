import os
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()

# Spotify authentication credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
playlist_id = '3xcL5K55RbI2PYzzsSbcBJ'

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Get playlist tracks
tracks = sp.playlist_items(playlist_id)

# Use RapidAPI Track Analyzer to fetch audio features
# Valence: Happiness, Danceability, Acousticness, Mode
# Arousal: Energy, Tempo, Loudness
features = []
for track in tracks['items']:
    track_id = track['track']['id']
    track_name = track['track']['name']
    track_artist = track['track']['artists'][0]['name']

    url = f'https://track-analysis.p.rapidapi.com/pktx/spotify/{track_id}'

    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': 'track-analysis.p.rapidapi.com'
    }

    time.sleep(2) # Respect API rate limits
    response = requests.get(url, headers=headers)
    result = response.json()

    # Extract relevant features
    features = {
        'id': track_id,
        'name': track_name,
        'artist': track_artist,
        'happiness': result.get('happiness'),
        'danceability': result.get('danceability'),
        'acousticness': result.get('acousticness'),
        'mode': result.get('mode'),
        'energy': result.get('energy'),
        'tempo': result.get('tempo'),
        'loudness': result.get('loudness')
    }

    # Export features to CSV
    with open('MoodFinder/data/track_features.csv', 'a') as f:
        if f.tell() == 0:
            f.write('id,name,artist,happiness,danceability,acousticness,mode,energy,tempo,loudness\n')
        f.write(f"{features['id']},{features['name']},{features['artist']},{features['happiness']},{features['danceability']},{features['acousticness']},{features['mode']},{features['energy']},{features['tempo']},{features['loudness']}\n")
