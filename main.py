import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from youtube_search import YoutubeSearch
import os
import requests
from io import BytesIO
from PIL import Image, ImageTk
import yt_dlp as youtube_dl
import re
import webbrowser

# This code is owned by Samir Nashed
# 03.08.2024

# Specify the path to ffmpeg
FFMPEG_PATH = "/usr/local/bin/ffmpeg"

# Function to search YouTube and return results
def search_youtube(query):
    results = YoutubeSearch(query, max_results=10).to_dict()
    return results

# Function to download the selected video and convert to MP3
def download_and_convert(url, download_path, title):
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
            'progress_hooks': [update_progress],  # Add progress hook
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        mp3_path = os.path.join(download_path, f'{sanitize_filename(title)}.mp3')

        progress_bar.stop()
        status_label.config(text="File is downloaded!")  # Update the status label
        return mp3_path
    except Exception as e:
        progress_bar.stop()
        status_label.config(text=f"Error: {str(e)}")
        return str(e)

# Progress hook to update status label and progress bar
def update_progress(d):
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

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)

def search_and_download():
    query = search_entry.get()
    if query:
        results = search_youtube(query)
        if results:
            show_results(results)
        else:
            messagebox.showinfo("No results", "No results found for your query.")
    else:
        messagebox.showinfo("Cancelled", "Search cancelled.")

def show_results(results):
    for widget in result_frame.winfo_children():
        widget.destroy()

    for i, result in enumerate(results):
        title = result['title']
        thumbnail_url = result['thumbnails'][0]
        url_suffix = result['url_suffix']

        frame = ttk.Frame(result_frame)
        frame.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky='ew')

        img_data = requests.get(thumbnail_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 75), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        thumbnail = tk.Label(frame, image=img)
        thumbnail.image = img
        thumbnail.pack(side='top')

        info_frame = ttk.Frame(frame)
        info_frame.pack(side='top', fill='x', expand=True)

        title_label = ttk.Label(info_frame, text=title)
        title_label.pack(anchor='w')

        url = 'https://www.youtube.com' + url_suffix
        play_button = ttk.Button(info_frame, text="Play in Browser", command=lambda url=url: webbrowser.open(url))
        play_button.pack(anchor='w', padx=5, pady=5)

        download_button = ttk.Button(info_frame, text="Download", command=lambda url=url, title=title: download(url, title))
        download_button.pack(anchor='w', padx=5, pady=5)

def download(url, title):
    download_path = os.path.expanduser("~/Downloads")
    result = download_and_convert(url, download_path, title)
    if os.path.exists(result):
        status_label.config(text=f"Downloaded and converted to MP3:\n{result}")
    else:
        messagebox.showerror("Error", f"Failed to download and convert:\n{result}")

root = tk.Tk()
root.title("YouTube to MP3 Converter")

# Create a style for the progress bar
style = ttk.Style()
style.theme_use('clam')  # Use 'clam' theme to allow customization
style.configure("green.Horizontal.TProgressbar", foreground='green', background='green', thickness=30)

# Create search frame
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

search_label = ttk.Label(search_frame, text="Search:")
search_label.grid(row=0, column=0)

search_entry = ttk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1)

search_button = ttk.Button(search_frame, text="Search", command=search_and_download)
search_button.grid(row=0, column=2)

# Create progress bar right under the search bar
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100, style="green.Horizontal.TProgressbar", length=400)
progress_bar.pack(pady=10, fill='x')

# Status label for messages
status_label = ttk.Label(root, text="", foreground="blue")
status_label.pack(pady=10)

result_frame = ttk.Frame(root)
result_frame.pack(fill='both', expand=True, padx=10, pady=10)

root.mainloop()
