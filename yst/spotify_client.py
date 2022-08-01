import requests
from urllib.parse import urlencode, urlparse
import urllib.parse
import json
import base64
import os

class SpotifyClient(object):
    def __init__(self, user_id):
        self.client_id = "aff6e6276dd34f6f8f4bc4020b842725"
        self.client_secret = "fe28f8899786414380729687453ee28f"
        try:
            with open("./creds/refresh_token.txt", "r+") as f:
                self.refresh_token = f.read()
        except:
            self.refresh_token = ""
        self.oauth_token = self.refreshed_access_key(self.refresh_token)
        self.user_id = user_id

    def get_auth_key(self):
        endpoint = "https://accounts.spotify.com/authorize"
        client_id = self.client_id
        client_secret = self.client_secret
        query_parameters = urlencode({
            "client_id" : client_id,
            "response_type": "code",
            "redirect_uri": "http://localhost:8000/callback/",
            "scope": "user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private"
        })
        url = f"{endpoint}?{query_parameters}"
        print(url)
        
        response_url = str(input("Please Copy And paste the URL: "))
        auth = urlparse(response_url)
        auth_key = auth[4].split("=")[1]
        return auth_key

    def get_access_key(self):
        endpoint = "https://accounts.spotify.com/api/token"
        auth_key = self.get_auth_key()
        client_id = self.client_id
        client_secret = self.client_secret

        data = {
            "grant_type": "authorization_code",
            "code" : auth_key,
            "redirect_uri": "http://localhost:8000/callback/",
            "client_id" : client_id,
            "client_secret" : client_secret
        }
        request = requests.post(endpoint, data=data)
        response = request.json()
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        with open("./creds/refresh_token.txt", "w") as f:
            f.write(refresh_token)
        return access_token, refresh_token

    def refreshed_access_key(self, refresh_token = ""):
        client_id = self.client_id
        client_secret = self.client_secret
        if refresh_token == "":
            return self.get_access_key()[0]
        if refresh_token:
            client_creds = f"{client_id}:{client_secret}"
            client_creds_encoded = base64.b64encode(client_creds.encode())
            client_creds_b64 = client_creds_encoded.decode()

            refresh_url = "https://accounts.spotify.com/api/token"
            data = {
                "grant_type" : "refresh_token",
                "refresh_token" : refresh_token
            }

            headers = {
                "Authorization" : f"Basic {client_creds_b64}"
            }
            request = requests.post(refresh_url, data = data, headers = headers)
            if request.status_code in range(200, 299):
                response = request.json()
                refreshed_access_token = response["access_token"]
                return refreshed_access_token
            else:
                return self.get_access_key()[0]

    def create_a_playlist(self, playlist_name):
        user_id = self.user_id
        oauth_token = self.oauth_token
        playlist_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        create_headers = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name" : playlist_name,
            "description" : "YEP COCK",
            "public" : "false"
        }
        r = requests.post(
            playlist_endpoint,
            headers=create_headers,
            data = json.dumps(data)
        )
        print(r.status_code)
        if r.status_code in range(200,299):
            r2 = requests.get(
                playlist_endpoint,
                headers = create_headers
            )
            response2 = r2.json()
            response2
            results = response2["items"]
            playlist_id = results[0]["id"]
            return playlist_id

    def search_song_and_return_uri(self, song_name):
        search_headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "Content-Type": "application/json"  
        }
        search_endpoint = "https://api.spotify.com/v1/search"
        call = urlencode({"q":f"{song_name}", "type":"track,artist"})
        search_url = f"{search_endpoint}?{call}"
        r = requests.get(search_url, headers = search_headers)
        response = r.json()
        result = response["tracks"]["items"]
        if result:
            song_name = result[0]["name"]
            song_uri = result[0]["uri"]
            if song_uri != None:
                return song_uri
        else:
            print("Couldn't Find Song")

    def add_song_to_playlist(self, playlist_id, song_uri):
        add_song_headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "Content-Type": "application/json"   
        }
        data = {
            "uris" : song_uri
        }
        add_song_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.post(
            add_song_endpoint,
            headers = add_song_headers,
            data = json.dumps(data)
        )
        print(r.status_code)

    def get_playlists(self):
        oauth_token = self.oauth_token
        user_id = self.user_id
        
        headers = {
            "Authorization": f"Bearer {oauth_token}"
        }
        query_parameters = urlencode({
            "limit" : 50
        })

        playlist_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists?{query_parameters}"
        r = requests.get(playlist_endpoint, headers=headers)
        response = r.json()
        results = response["items"]
        spotify_playlists = []
        for result in results:
            playlist_id = result["id"]
            playlist_name = result["name"]
            spotify_playlists.append((playlist_id,playlist_name))
        return spotify_playlists

    def get_songs_from_playlist(self, playlist_id):
        playlist_id = playlist_id
        songs_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.oauth_token}"
        }

        r = requests.get(songs_endpoint, headers=headers)
        response = r.json()
        results = response["items"]
        playlist_songs = []
        for result in results:
            artist_name = result["track"]["artists"][0]["name"]
            song_name = result["track"]["name"]
            playlist_songs.append((f"{artist_name} {song_name}"))
        return playlist_songs
