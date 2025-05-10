# yoohoo.py

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, Label, Progressbar
from utils.downloader import download_video

class YooHooApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YooHoo - YouTube Downloader")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.save_path = os.path.expanduser("~/Downloads")
        self.style = Style("vapor")  

        self.create_widgets()

    def create_widgets(self):
        Label(text="⚠️ WARNING: Please do not complain about the download speed.\nIt depends on your OWN internet connectivity.",
              wraplength=480,
              foreground="red").pack(pady=(10, 5))

        self.url_entry = Entry(width=50)
        self.url_entry.pack(pady=(5, 5))

        self.format_var = tk.StringVar(value="mp4")
        tk.OptionMenu(self.root, self.format_var, "mp4", "mp3").pack()

        self.choose_path_button = Button(text="Choose Download Folder", command=self.choose_path)
        self.choose_path_button.pack(pady=(5, 5))

        self.download_button = Button(text="Download", command=self.start_download)
        self.download_button.pack(pady=(5, 10))

        self.progress = Progressbar(length=400, mode="determinate")
        self.progress.pack(pady=(5, 5))

    def choose_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path = path

    def start_download(self):
        url = self.url_entry.get()
        fmt = self.format_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        self.download_button.config(state="disabled")
        self.url_entry.config(state="disabled")
        self.choose_path_button.config(state="disabled")

        threading.Thread(target=self.download_worker, args=(url, fmt), daemon=True).start()

    def download_worker(self, url, fmt):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0%').strip('%')
                try:
                    self.progress['value'] = float(percent)
                except:
                    pass
            elif d['status'] == 'finished':
                self.progress['value'] = 100

        success = download_video(url, fmt, self.save_path, progress_hook)

        self.progress['value'] = 0
        self.download_button.config(state="normal")
        self.url_entry.config(state="normal")
        self.choose_path_button.config(state="normal")

        if success:
            messagebox.showinfo("Success", f"Downloaded to {self.save_path}")
        else:
            messagebox.showerror("Failure", "Download failed. Check your URL or format.")

if __name__ == '__main__':
    root = tk.Tk()
    app = YooHooApp(root)
    root.mainloop()

