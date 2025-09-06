import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

# Spotify authentication credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
playlist_id = '3xcL5K55RbI2PYzzsSbcBJ'

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Get playlist items and extract track IDs
tracks = sp.playlist_items(playlist_id)
track_ids = [item['track']['id'] for item in tracks['items'] if item['track']]
