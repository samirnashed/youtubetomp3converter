# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import os
from search_youtube import search_youtube, show_video_thumbnail_and_confirm
from download_convert import download_and_convert
import re
root = tk.Tk()

# Example text entry for a YouTube URL
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

# Button to trigger showing the video thumbnail and asking for confirmation
confirm_button = tk.Button(root, text="Show Video and Confirm", command=lambda: show_video_thumbnail_and_confirm(url_entry.get(), root))
confirm_button.pack(pady=10)

root.mainloop()

def search_and_download(search_entry, result_frame, status_label, progress_bar, root):
    query = search_entry.get()
    if query:
        results = search_youtube(query)
        if results:
            show_results(results, result_frame, status_label, progress_bar, root)
        else:
            messagebox.showinfo("No results", "No results found for your query.")
    else:
        messagebox.showinfo("Cancelled", "Search cancelled.")

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
