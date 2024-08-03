# download_convert.py
import os
import re
from yt_dlp import YoutubeDL
import tkinter as tk

FFMPEG_PATH = "/usr/local/bin/ffmpeg"

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)

def update_progress(d, status_label, progress_bar, root):
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

def download_and_convert(url, download_path, title, status_label, progress_bar, root):
    try:
        status_label.config(text="Downloading...")
        progress_bar.start()
        root.update()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, f'{sanitize_filename(title)}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'ffmpeg_location': FFMPEG_PATH,
            'progress_hooks': [lambda d: update_progress(d, status_label, progress_bar, root)],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        mp3_path = os.path.join(download_path, f'{sanitize_filename(title)}.mp3')

        progress_bar.stop()
        status_label.config(text="File is downloaded!")
        return mp3_path
    except Exception as e:
        progress_bar.stop()
        status_label.config(text=f"Error: {str(e)}")
        return str(e)
