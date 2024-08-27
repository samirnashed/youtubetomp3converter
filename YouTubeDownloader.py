import os
import re
import yt_dlp as youtube_dl
from youtube_search import YoutubeSearch  # Ensure this is installed via pip

class YouTubeDownloader:
    def __init__(self, ffmpeg_path="/usr/local/bin/ffmpeg"):
        self.ffmpeg_path = ffmpeg_path

    def sanitize_filename(self, title):
        """Sanitize the title to be a valid filename."""
        return re.sub(r'[<>:"/\\|?*]', '', title)

    def download_and_convert(self, url, download_path, title, status_label, progress_bar, root):
        """Download and convert a YouTube video to MP3."""
        try:
            status_label.config(text="Downloading...")
            progress_bar.start()
            root.update()

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(download_path, f'{self.sanitize_filename(title)}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self.update_progress(status_label, progress_bar, root)],  # Add progress hook
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_path = os.path.join(download_path, f'{self.sanitize_filename(title)}.mp3')

            progress_bar.stop()
            status_label.config(text="File is downloaded!")  # Update the status label
            return mp3_path
        except Exception as e:
            progress_bar.stop()
            status_label.config(text=f"Error: {str(e)}")
            return str(e)

    def update_progress(self, status_label, progress_bar, root):
        """Return a progress hook function for yt-dlp."""
        def hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes:
                    percent = int(downloaded_bytes / total_bytes * 100)
                    status_label.config(text=f"Downloading... {percent}% complete")
                    progress_bar['value'] = percent
                    root.update()
            elif d['status'] == 'finished':
                status_label.config(text="Download finished, now converting...")
                progress_bar.stop()
                root.update()
        return hook
    
    def search_youtube(query):
        results = YoutubeSearch(query).to_dict()
        return results
