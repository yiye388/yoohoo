# utils/downloader.py

import yt_dlp
import os

def download_video(url, format='mp4', output_path=None, hook=None):
    """Download a video using yt-dlp."""
    if not output_path:
        output_path = os.path.expanduser("~/Downloads")

    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }

    if hook:
        ydl_opts['progress_hooks'] = [hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

