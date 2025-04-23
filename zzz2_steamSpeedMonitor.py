import os
import time

DOWNLOAD_FOLDER = r"D:\Steam\steamapps\downloading"

def get_largest_file(path):
    latest_file = None
    latest_size = 0
    latest_mtime = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                mtime = os.path.getmtime(fp)
                size = os.path.getsize(fp)
                if mtime > latest_mtime:
                    latest_file = fp
                    latest_mtime = mtime
                    latest_size = size
            except (FileNotFoundError, PermissionError):
                continue
    return latest_file, latest_size

def format_speed(bytes_per_sec):
    gb_per_sec = bytes_per_sec / (1024**3)
    mb_per_sec = bytes_per_sec / (1024**2)
    mb_per_min = mb_per_sec * 60
    return f"{gb_per_sec:.3f} GB/s | {mb_per_sec:.1f} MB/s | {mb_per_min:.0f} MB/min"

def monitor_file_growth(path, interval=1.0):
    print(f"Monitoring file write speed in:\n{path}\n(Press Ctrl+C to stop)\n")
    file_path, prev_size = get_largest_file(path)
    if not file_path:
        print("No active file found.")
        return

    print(f"Tracking file: {file_path}")
    try:
        while True:
            time.sleep(interval)
            try:
                curr_size = os.path.getsize(file_path)
                bytes_diff = curr_size - prev_size
                speed = format_speed(bytes_diff / interval)
                print(f"[{time.strftime('%H:%M:%S')}] {speed}")
                prev_size = curr_size
            except FileNotFoundError:
                print("File no longer exists - waiting for new download...")
                file_path, prev_size = get_largest_file(path)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    monitor_file_growth(DOWNLOAD_FOLDER)
