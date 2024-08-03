# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import os
import yt_dlp as youtube_dl
from search_youtube import search_youtube
from download_convert import download_and_convert

def handle_search_or_link(input_text, result_frame, status_label, progress_bar, root):
    if "youtube.com" in input_text or "youtu.be" in input_text:
        fetch_video_details(input_text, status_label, progress_bar, root)
    else:
        search_and_download(input_text, result_frame, status_label, progress_bar, root)

def search_and_download(query, result_frame, status_label, progress_bar, root):
    results = search_youtube(query)
    if results:
        show_results(results, result_frame, status_label, progress_bar, root)
    else:
        messagebox.showinfo("No results", "No results found for your query.")

def show_results(results, result_frame, status_label, progress_bar, root):
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

        download_button = ttk.Button(info_frame, text="Download", command=lambda url=url, title=title: download(url, title, status_label, progress_bar, root))
        download_button.pack(anchor='w', padx=5, pady=5)

def download(url, title, status_label, progress_bar, root):
    download_path = os.path.expanduser("~/Downloads")
    result = download_and_convert(url, download_path, title, status_label, progress_bar, root)
    if os.path.exists(result):
        status_label.config(text=f"Downloaded and converted to MP3:\n{result}")
    else:
        messagebox.showerror("Error", f"Failed to download and convert:\n{result}")

def fetch_video_details(url, status_label, progress_bar, root):
    ydl_opts = {'quiet': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'Unknown Title')
        thumbnail_url = info_dict.get('thumbnail')

    confirm_download(url, title, thumbnail_url, status_label, progress_bar, root)

def confirm_download(url, title, thumbnail_url, status_label, progress_bar, root):
    def on_confirm():
        download(url, title, status_label, progress_bar, root)
        confirm_window.destroy()

    confirm_window = tk.Toplevel(root)
    confirm_window.title("Confirm Download")

    thumbnail_data = requests.get(thumbnail_url).content
    thumbnail_img = Image.open(BytesIO(thumbnail_data))
    thumbnail_img = thumbnail_img.resize((200, 150), Image.LANCZOS)
    thumbnail_img = ImageTk.PhotoImage(thumbnail_img)

    thumbnail_label = tk.Label(confirm_window, image=thumbnail_img)
    thumbnail_label.image = thumbnail_img
    thumbnail_label.pack(pady=10)

    title_label = ttk.Label(confirm_window, text=title, wraplength=300)
    title_label.pack(pady=10)

    button_frame = ttk.Frame(confirm_window)
    button_frame.pack(pady=10)

    confirm_button = ttk.Button(button_frame, text="Confirm", command=on_confirm)
    confirm_button.pack(side=tk.LEFT, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=confirm_window.destroy)
    cancel_button.pack(side=tk.LEFT, padx=5)
