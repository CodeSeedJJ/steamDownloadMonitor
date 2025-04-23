import os
import time
from pathlib import Path

def get_largest_file(folder):
    files = list(Path(folder).glob('*'))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_size if f.is_file() else 0)

def format_speed(bytes_per_sec):
    gb_per_sec = bytes_per_sec / (1024 ** 3)
    mb_per_sec = bytes_per_sec / (1024 ** 2)
    mb_per_min = mb_per_sec * 60
    return f"{gb_per_sec:.3f} GB/s | {mb_per_sec:.1f} MB/s | {int(mb_per_min)} MB/min"

def monitor_file_growth(folder, interval=1):
    print("Monitoring file write speed in:")
    print(folder)
    print("(Press Ctrl+C to stop)\n")

    active_file = get_largest_file(folder)
    if not active_file:
        print("No active file found.")
        return

    print(f"Tracking file: {active_file}")

    try:
        prev_size = active_file.stat().st_size
        while True:
            time.sleep(interval)
            if not active_file.exists():
                print("File no longer exists - waiting for new download...")
                time.sleep(2)
                active_file = get_largest_file(folder)
                if not active_file:
                    continue
                prev_size = active_file.stat().st_size
                print(f"Tracking new file: {active_file}")
                continue

            curr_size = active_file.stat().st_size
            speed_bps = (curr_size - prev_size) / interval
            print(f"[{time.strftime('%H:%M:%S')}] {format_speed(speed_bps)}")
            prev_size = curr_size
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    DOWNLOAD_FOLDER = r"D:\\Steam\\steamapps\\downloading"
    monitor_file_growth(DOWNLOAD_FOLDER)
