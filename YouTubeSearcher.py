import os
import re
import yt_dlp as youtube_dl
from youtube_search import YoutubeSearch  # Ensure this is installed via pip

class YouTubeSearcher:
    def __init__(self):
        pass
    def search_youtube(self,query):
        results = YoutubeSearch(query).to_dict()
        return results
    
    def fetch_video_details(url):
        ydl_opts = {'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            return title
    def get_video_title(self, url):
        ydl_opts = {'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            return title