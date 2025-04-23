import tkinter as tk
from tkinter import ttk
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# This function will simulate checking the Steam download speed and update the GUI
def check_download_speed():
    speeds = []  # Store the download speeds to adjust the graph dynamically
    max_speed = 10  # Set an initial maximum speed (adjust as needed)

    while monitoring:  # This is a global variable that controls whether we're monitoring
        # Simulate speed (for testing, replace with actual logic like log parsing or file tracking)
        current_speed = random.uniform(0, 5)  # Placeholder value, in MB/s, randomly generated for demo
        speeds.append(current_speed)

        # Adjust the maximum speed if the current speed exceeds the previous max
        max_speed = max(max_speed, max(speeds))

        # Update GUI with current values
        download_speed_label.config(text=f"Download Speed: {current_speed:.2f} MB/s")
        total_downloaded_label.config(text=f"Total Downloaded: {sum(speeds):.2f} MB")
        
        # Plot the graph
        plot_graph(speeds, max_speed)

        # Wait for the next update (1 second)
        time.sleep(1)

# Function to plot the graph
def plot_graph(speeds, max_speed):
    fig.clear()
    ax = fig.add_subplot(111)

    # Plot the download speeds
    ax.plot(speeds, label="Download Speed (MB/s)", color="green")

    # Set labels and title
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Download Speed (MB/s)")
    ax.set_title("Steam Download Speed Over Time")

    # Adjust the y-axis to match the observed data range
    ax.set_ylim(0, max_speed * 1.1)  # Give a little buffer above the max speed

    # Update the canvas with the new graph
    canvas.draw()

# Start monitoring function
def start_monitoring():
    global monitoring
    monitoring = True
    # Disable the "Start" button and enable the "Stop" button
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    
    # Start the download speed check in a separate thread
    threading.Thread(target=check_download_speed, daemon=True).start()

# Stop monitoring function
def stop_monitoring():
    global monitoring
    monitoring = False
    # Disable the "Stop" button and enable the "Start" button
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Set up the basic window
window = tk.Tk()
window.title("Steam Download Speed Monitor")
window.geometry("600x400")
window.configure(bg="grey")

# Labels to show speed, total downloaded, and time remaining
download_speed_label = ttk.Label(window, text="Download Speed: -- MB/s", font=("Arial", 14), background="grey", foreground="white")
download_speed_label.pack(pady=10)

total_downloaded_label = ttk.Label(window, text="Total Downloaded: -- MB", font=("Arial", 14), background="grey", foreground="white")
total_downloaded_label.pack(pady=10)

# Start and Stop buttons
start_button = ttk.Button(window, text="Start Monitoring", command=start_monitoring)
start_button.pack(side=tk.LEFT, padx=20, pady=20)

stop_button = ttk.Button(window, text="Stop Monitoring", command=stop_monitoring, state=tk.DISABLED)
stop_button.pack(side=tk.RIGHT, padx=20, pady=20)

# Create a figure and canvas for the graph
fig = plt.Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(pady=10)

# Run the application
window.mainloop()
