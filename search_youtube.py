# combined_utils.py
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
from io import BytesIO

from youtube_search import YoutubeSearch  # Ensure this is installed via pip

def search_youtube(query, max_results=10):
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    return results