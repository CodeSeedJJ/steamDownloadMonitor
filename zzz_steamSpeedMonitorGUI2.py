import tkinter as tk
from tkinter import ttk
import os
import time
import threading
import re

LOG_PATH = os.path.expanduser("D:\\Steam\\logs\\content_log.txt")
BYTES_PER_MB = 1024 * 1024

class SteamSpeedMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Download Speed Monitor")
        self.root.geometry("400x200")

        self.label = ttk.Label(root, text="Speed: Initializing...", font=("Consolas", 18))
        self.label.pack(expand=True)

        self.last_size = 0
        self.last_time = time.time()
        self.total_written = 0
        self.running = True

        threading.Thread(target=self.monitor_log, daemon=True).start()

    def monitor_log(self):
        if not os.path.exists(LOG_PATH):
            self.update_label("Log not found.")
            return

        with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            f.seek(0, os.SEEK_END)  # start at end of file
            while self.running:
                line = f.readline()
                if not line:
                    time.sleep(0.2)
                    continue

                match = re.search(r"bytes written = (\\d+)", line)
                if match:
                    bytes_written = int(match.group(1))
                    now = time.time()
                    elapsed = now - self.last_time

                    if elapsed >= 1:
                        mbps = (bytes_written / BYTES_PER_MB) / elapsed
                        self.update_label(f"Speed: {mbps:.2f} MB/s")
                        self.last_time = now

    def update_label(self, text):
        self.label.after(0, self.label.config, {"text": text})

    def stop(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = SteamSpeedMonitor(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop(), root.destroy()))
    root.mainloop()
