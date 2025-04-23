import tkinter as tk
from tkinter import ttk
import time
import threading
import re

# Log file path for Steam content log
LOG_FILE_PATH = r'D:\Steam\logs\content_log.txt'

# Shared variable to control monitoring
monitoring = False

def extract_download_rate(line):
    """Extract the current download rate from a log line."""
    match = re.search(r'Current download rate: (\d+\.\d+) Mbps', line)
    if match:
        return float(match.group(1))
    return None

def monitor_log_for_speed():
    """Monitor Steam log file for current download rate."""
    with open(LOG_FILE_PATH, 'r') as file:
        file.seek(0, 2)  # Move to end of file

        while monitoring:
            line = file.readline()
            if line:
                download_rate = extract_download_rate(line)
                if download_rate is not None:
                    mb_per_s = download_rate / 8
                    gb_per_s = mb_per_s / 1024
                    
                    download_speed_label.config(text=f"Download Speed: {mb_per_s:.2f} MB/s ({gb_per_s:.3f} GB/s)")
                
            else:
                time.sleep(1)

def start_monitoring():
    global monitoring
    monitoring = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    threading.Thread(target=monitor_log_for_speed, daemon=True).start()

def stop_monitoring():
    global monitoring
    monitoring = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# GUI setup
window = tk.Tk()
window.title("Steam Download Speed Monitor")
window.geometry("400x150")

download_speed_label = ttk.Label(window, text="Download Speed: --", font=("Arial", 14))
download_speed_label.pack(pady=20)

start_button = ttk.Button(window, text="Start Monitoring", command=start_monitoring)
start_button.pack(side=tk.LEFT, padx=20, pady=20)

stop_button = ttk.Button(window, text="Stop Monitoring", command=stop_monitoring, state=tk.DISABLED)
stop_button.pack(side=tk.RIGHT, padx=20, pady=20)

window.mainloop()
