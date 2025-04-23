import os
import time

DOWNLOAD_FOLDER = r"D:\Steam\steamapps\downloading"

def get_folder_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
            except FileNotFoundError:
                continue  # Handle deleted files mid-read
    return total

def format_speed(bytes_per_sec):
    gb_per_sec = bytes_per_sec / (1024**3)
    mb_per_sec = bytes_per_sec / (1024**2)
    mb_per_min = mb_per_sec * 60
    return f"{gb_per_sec:.3f} GB/s | {mb_per_sec:.1f} MB/s | {mb_per_min:.0f} MB/min"

def monitor_download_speed(path, interval=1.0):
    print(f"Monitoring Steam download speed in:\n{path}\n(Press Ctrl+C to stop)\n")
    prev_size = get_folder_size(path)
    try:
        while True:
            time.sleep(interval)
            curr_size = get_folder_size(path)
            bytes_diff = curr_size - prev_size
            speed = format_speed(bytes_diff / interval)
            print(f"[{time.strftime('%H:%M:%S')}] {speed}")
            prev_size = curr_size
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    monitor_download_speed(DOWNLOAD_FOLDER)
