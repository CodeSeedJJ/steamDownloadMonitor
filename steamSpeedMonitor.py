import time
import re

# Define log file path
LOG_FILE_PATH = r'D:\Steam\logs\content_log.txt'

def extract_download_rate(line):
    """Extract the current download rate from a log line."""
    match = re.search(r'Current download rate: (\d+\.\d+) Mbps', line)
    if match:
        return float(match.group(1))
    return None

def monitor_log_for_speed():
    """Monitor Steam log file for current download rate."""
    with open(LOG_FILE_PATH, 'r') as file:
        # Go to the end of the file to avoid reading old logs
        file.seek(0, 2)
        
        while True:
            line = file.readline()
            if line:
                download_rate = extract_download_rate(line)
                if download_rate is not None:
                    # Convert Mbps to MB/s
                    mb_per_s = download_rate / 8
                    gb_per_s = mb_per_s / 1024
                    print(f'Download rate: {download_rate} Mbps | {mb_per_s:.3f} MB/s | {gb_per_s:.3f} GB/s')
            else:
                time.sleep(1)  # Wait for new lines to be added to the log

if __name__ == '__main__':
    monitor_log_for_speed()
