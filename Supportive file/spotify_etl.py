import spotipy
import pandas as pd 
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import s3fs 

def run_spotify_etl():

    client_id = "b8db1f5e394149a69d57283ea2e75761"
    client_secret = "93425fac35e94d59b6a90f6714443668"
# Provide details for authentication to extract data from spotify
    client_credentials_mgr = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
    

    # Create an object to provides authorization to access data to extract
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_mgr)

    playlist_link = "https://open.spotify.com/playlist/7oFbQJn36KPaMHEwgT1XF4"
    playlist_URI = playlist_link.split('/')[-1]

    # To extract all the info related to tracks
    data = sp.playlist_tracks(playlist_URI)

    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        
        album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                        'total_tracks':album_total_tracks,'url':album_url}
        album_list.append(album_element)
    album_df = pd.DataFrame.from_dict(album_list)

    artist_list = []
    for row in data['items']:
        for key,value in row.items():
            if key == 'track':
                for artist in value['artists']:
                    artist_dict = {'artist_id':artist['id'],'artist_name':artist['name'],'externam_url':artist['external_urls']['spotify']}
                    artist_list.append(artist_dict)
    artist_df = pd.DataFrame.from_dict(artist_list)
    
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_dict = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                    'popularity':song_popularity,'song_added':song_added,'album_id':album_id,'artist_id':artist_id}
        song_list.append(song_dict)
    song_df = pd.DataFrame.from_dict(song_list)


    album_df = album_df.drop_duplicates(subset='album_id')
    artist_df = artist_df.drop_duplicates(subset='artist_id')
    song_df = song_df.drop_duplicates(subset='song_id')

    album_df.to_csv("s3://spotifydatabucket/album.csv")
    artist_df.to_csv("s3://spotifydatabucket/artist_df.csv")
    song_df.to_csv("s3://spotifydatabucket/song_df.csv")