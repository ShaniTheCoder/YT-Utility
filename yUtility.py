import requests
from os.path import isdir
from shutil import copyfileobj
from urllib.parse import urlparse
from pytube import YouTube, Playlist

class YoutubeUtility:
    def __init__(self, url, download_path) -> None:
        self.url = url
        self.download_path = download_path
        self.yt = YouTube(self.url)

    def download_youtube_thumbnail(self):
        thumbnail = self.yt.thumbnail_url
        parsed_url = urlparse(thumbnail)
        file_name = parsed_url.path.split("/")[-1]
        save_path = f"{self.download_path}/{file_name}" if self.download_path else file_name
        request = requests.get(thumbnail, stream=True)
        if request.status_code == 200:
            with open(save_path, 'wb') as file:
                request.raw.decode_content = True
                copyfileobj(request.raw, file)
                print('Thumbnail downloaded')
            return save_path
        else:
            print(f'Unable to download thumbnail, error code - {request.status_code}')
            return None

    def download_youtube_video(self):
        stream = self.yt.streams.get_highest_resolution()
        video_path = stream.download(self.download_path)
        return video_path

    def download_playlist_videos(self):
        playlist = Playlist(self.url)
        for video in playlist.videos:
            try:
                stream = video.streams.get_highest_resolution()
                print(f"Downloading {video.title}...")
                stream.download(self.download_path)
                print(f"{video.title} downloaded successfully!")
            except Exception as e:
                print(f"Error downloading {video}: {e}")

    def get_video_title(self):
        try:
            return self.yt.title
        except Exception as e:
            print(f"Error getting video title: {e}")
            return None

if __name__ == '__main__':
    yt = YoutubeUtility("https://youtu.be/A74TOX803D0?si=kmmbo5CysSSn_g_z","/")
    yt.download_youtube_video()
