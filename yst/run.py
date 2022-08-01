import os

from youtube_client import YoutubeClient
from spotify_client import SpotifyClient

def run():
    spotify_user_id = "karasakiz.baris"
    def youtube_to_spotify():
        playlists = youtube_client.get_playlist()
        for index, playlist in enumerate(playlists):
            print(f"{index}: {playlist[1]}")
        try:
            to_spotify = int(input("Which playlist do you want to import to Spotify?: "))
            if to_spotify in range(len(playlists)):
                chosen_playlist = playlists[to_spotify]
                youtube_playlist_id = chosen_playlist[0]
                youtube_playlist_name = chosen_playlist[1]
                print(youtube_playlist_id, youtube_playlist_name)
                songs = youtube_client.get_songs_from_playlist(youtube_playlist_id)
                uri_list = []
                for song in songs:
                    song_uri = spotify_client.search_song_and_return_uri(song)
                    #print(song_uri)
                    if song_uri != None:
                        uri_list.append(song_uri)
                print(uri_list)
                spotify_playlist_id = spotify_client.create_a_playlist(youtube_playlist_name)
                song_added = spotify_client.add_song_to_playlist(spotify_playlist_id, uri_list)
            else:
                youtube_to_spotify()
        except:
            youtube_to_spotify()

    def spotify_to_mp3():
        playlists = spotify_client.get_playlists()
        for index, playlist in enumerate(playlists):
            print(f"{index}: {playlist[1]}")
        try:
            choice = int(input("Choose a playlist to download: "))
            if choice in range(len(playlists)):
                playlist_to_download = playlists[choice]
                print(playlist_to_download)
                chosen_playlist_id = playlist_to_download[0]
                chosen_playlist_name = playlist_to_download[1]
                songs = spotify_client.get_songs_from_playlist(chosen_playlist_id)
                video_ids = []
                for song in songs:
                    video_id = youtube_client.search_songs_on_youtube(song)
                    video_ids.append(video_id)
                for _id in video_ids:
                    youtube_client.download_youtube_videos_as_mp3(_id, chosen_playlist_name)
                print("Download Finished")
            else:
                spotify_to_mp3()
        except:
            spotify_to_mp3()

    youtube_client = YoutubeClient("./creds/client_secret.json")
    spotify_client = SpotifyClient(spotify_user_id)
    while True:
        try:
            choice = input("To import your Youtube playlist to Spotify press 1, To download from your Spotify playlists press 2, to exit write 'exit': ")
        except:
            print("Please make a choice.")
            continue 
        if choice == "1":
            youtube_to_spotify()
        if choice == "2":
            spotify_to_mp3()
        if choice == "exit":
            break
if __name__ == "__main__":
    run()
