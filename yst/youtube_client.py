import youtube_dl
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
import os

class YoutubeClient(object):
    def __init__(self, creds):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = creds

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes
            )
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
            )
        self.youtube = youtube

    def get_playlist(self):
        request = self.youtube.playlists().list(
            part = "id,snippet",
            mine = True,
            maxResults = 100
        )
        response = request.execute()
        playlists = []
        results  = response["items"]
        for result in results:
            playlist_title = result["snippet"]["title"]
            playlist_id = result["id"]
            playlists.append((playlist_id, playlist_title))
        return playlists

    def get_songs_from_playlist(self, playlist_id):
        request = self.youtube.playlistItems().list(
            playlistId = playlist_id,
            part = "id, snippet",
            maxResults = 100
        )
        response = request.execute()
        results = response["items"]
        songs = []
        for result in results:
            video_id = result["snippet"]["resourceId"]["videoId"]
            video_title = result["snippet"]["title"]
            songs.append(video_title)
        print(songs)
        clean_titles = []
        forbids = ["(", "[", "Official", "OFFICIAL", "Lyrics", "Lyric", "Video", "VIDEO"]
        for song in songs: 
            song = song.replace("-"," ")
            for let in forbids:
                if let in song:
                    new_title = song.split(let)
                    song = new_title[0]
            clean_titles.append(song)
        print(clean_titles)
        return clean_titles

    def download_youtube_videos_as_mp3(self, video_id, playlist_name):
        cwd = os.getcwd()
        DATA_DIR = os.path.join(cwd, "youtube_mp3")
        FILE_DIR = os.path.join(DATA_DIR, f"{playlist_name}")
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(FILE_DIR, exist_ok=True)

        video_id = video_id
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        video = youtube_dl.YoutubeDL().extract_info(
            youtube_url, download=False
        )
        title = video["title"]
        filename = f"{title}.mp3"
        options = {
            "format":"bestaudio/best",
            "keepvideo": False,
            "outtmpl" : os.path.join(FILE_DIR, filename),
            "postproccessors":[{
                "key": "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality": "192"
            }]
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video["webpage_url"]])

    def search_songs_on_youtube(self, song_title):
        spotify_song_title = song_title
        
        request = self.youtube.search().list(
            part = "id",
            maxResults = 1,
            q= f"{spotify_song_title}",
            fields="items/id/videoId"
        )
        response = request.execute()
        results = response["items"]
        search_vid_id = results[0]["id"]["videoId"]
        return search_vid_id
