# main.py
import tkinter as tk
from tkinter import ttk
from gui import handle_search_or_link

root = tk.Tk()
root.title("YouTube to MP3 Converter")

# Create a style for the progress bar
style = ttk.Style()
style.theme_use('clam')  # Use 'clam' theme to allow customization
style.configure("green.Horizontal.TProgressbar", foreground='green', background='green', thickness=30)

# Create search frame
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

search_label = ttk.Label(search_frame, text="Search or Paste Link:")
search_label.grid(row=0, column=0)

search_entry = ttk.Entry(search_frame, width=50)
search_entry.grid(row=0, column=1)

search_button = ttk.Button(search_frame, text="Go", command=lambda: handle_search_or_link(search_entry.get(), result_frame, status_label, progress_bar, root))
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
