import os
from io import BytesIO
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

from YouTubeDownloader import YouTubeDownloader
from YouTubeSearcher import YouTubeSearcher
class YouTubeToMP3App:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to MP3 Converter")
        self.root.geometry("900x600")

        # Initialize main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        # Initialize canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Initialize scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Initialize result frame
        self.result_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.result_frame, anchor='nw')

        # Bind mouse scroll to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Windows and MacOS
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)    # Linux scroll down

        # Initialize bottom frame for search and buttons
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(fill='x')

        # Add search bar and buttons to bottom_frame
        self.setup_bottom_frame()

        # Initialize progress bar and status label
        self.progress_bar = ttk.Progressbar(self.bottom_frame, orient='horizontal', mode='determinate', maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=3, pady=5, padx=10, sticky='ew')

        self.status_label = ttk.Label(self.bottom_frame, text="Status: Ready")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=(0, 10))

        # Initialize YouTubeDownloader instance
        self.downloader = YouTubeDownloader()

        self.searcher = YouTubeSearcher()

    def setup_bottom_frame(self):
        """Setup the bottom frame with search entry and buttons."""
        search_label = ttk.Label(self.bottom_frame, text="Search or Paste Link:")
        search_label.grid(row=0, column=0, padx=(10, 5))

        self.search_entry = ttk.Entry(self.bottom_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=(0, 5))

        search_button = ttk.Button(self.bottom_frame, text="Go", command=self.perform_search)
        search_button.grid(row=0, column=2, padx=(0, 10))

    def perform_search(self):
        """Perform the YouTube search and show results."""
        query = self.search_entry.get()

        if "youtube.com" in query or "youtu.be" in query:
            if "list=" in query:
                # self.fetch_playlist_details(input_text)
                pass
            else:
                title= self.searcher.get_video_title(query)
                self.download(query,title)

        else:
            results = self.searcher.search_youtube(query)  # Assuming this function returns a list of results
            self.show_results(results)


    def show_results(self, results):
        """Display search results in the result frame."""
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Configure the grid layout to make it scrollable
        for col in range(3):
            self.result_frame.grid_columnconfigure(col, weight=1)

        # Estimate the number of characters per line based on wraplength
        max_chars_per_line = 30  # Adjust this number based on actual wraplength and font size
        max_lines = 3
        max_chars = max_chars_per_line * max_lines

        for i, result in enumerate(results):
            title = result['title']
            thumbnail_url = result['thumbnails'][0]
            url_suffix = result['url_suffix']

            # Truncate title to fit within 3 lines
            if len(title) > max_chars:
                title = title[:max_chars - 3] + "..."  # Truncate and add ellipsis

            # Create a frame for each result and place it in the grid
            frame = ttk.Frame(self.result_frame)
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky='nsew')

            try:
                # Fetch and display the thumbnail image
                img_data = requests.get(thumbnail_url).content
                img = Image.open(BytesIO(img_data))
                img = img.resize((150, 100), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)

                thumbnail = tk.Label(frame, image=img)
                thumbnail.image = img  # Keep a reference to avoid garbage collection
                thumbnail.grid(row=0, column=0, columnspan=2, pady=5)
            except Exception as e:
                print(f"Error loading thumbnail: {e}")

            # Add a title label with a fixed height for 3 lines
            title_label = tk.Label(frame, text=title, wraplength=150, height=3, anchor='w', justify='left')
            title_label.grid(row=1, column=0, columnspan=2, pady=5, sticky='w')

            # Create a "Download" button
            download_button = ttk.Button(frame, text="Download", command=lambda url='https://www.youtube.com' + url_suffix, title=title: self.download(url, title))
            download_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Update the status label
        self.status_label.config(text="Search complete. Select an option to download.")

    def download(self, url, title):
        """Handle downloading of the video."""
        # Example download path
        download_path = os.path.expanduser("~")  # For demonstration, using user's home directory
        self.downloader.download_and_convert(url, download_path, title, self.status_label, self.progress_bar, self.root)

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        # Windows and macOS scroll
        if event.delta:
            self.canvas.yview_scroll(-1 * event.delta, "units")
        # Linux scroll
        elif event.num == 4:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            self.canvas.yview_scroll(1, "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeToMP3App(root)
    root.mainloop()