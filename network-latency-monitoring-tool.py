# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 05:54:47 2024

@author: IAN CARTER KULANI
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ping3 import ping

class LatencyMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Latency Monitor")
        self.root.geometry("600x500")
        
        self.ip_address = tk.StringVar()
        self.latency_data = []
        self.time_data = []
        self.is_monitoring = False

        self.create_widgets()

    def create_widgets(self):
        # Entry to input IP address
        ttk.Label(self.root, text="Enter IP Address or Hostname:").grid(row=0, column=0, padx=10, pady=5)
        self.ip_entry = ttk.Entry(self.root, textvariable=self.ip_address, width=30)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)

        # Button to start/stop monitoring
        self.start_button = ttk.Button(self.root, text="Start Monitoring", command=self.toggle_monitoring)
        self.start_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Label to show current latency
        self.latency_label = ttk.Label(self.root, text="Current Latency: -- ms")
        self.latency_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Matplotlib plot
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.ax.set_title("Latency Over Time")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Latency (ms)")
        self.ax.set_ylim(0, 1000)  # Set y-axis range for latency

        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def toggle_monitoring(self):
        if self.is_monitoring:
            self.is_monitoring = False
            self.start_button.config(text="Start Monitoring")
        else:
            self.is_monitoring = True
            self.start_button.config(text="Stop Monitoring")
            threading.Thread(target=self.monitor_latency).start()

    def monitor_latency(self):
        start_time = time.time()
        while self.is_monitoring:
            ip = self.ip_address.get()
            if ip:
                latency = self.ping_ip(ip)
                if latency is not None:
                    self.update_latency(latency, time.time() - start_time)
                time.sleep(1)

    def ping_ip(self, ip):
        try:
            latency = ping(ip)
            if latency is not None:
                return round(latency * 1000)  # Convert seconds to milliseconds
        except Exception as e:
            print(f"Error pinging IP: {e}")
        return None

    def update_latency(self, latency, time_elapsed):
        self.latency_data.append(latency)
        self.time_data.append(time_elapsed)

        # Update the latency label
        self.latency_label.config(text=f"Current Latency: {latency} ms")

        # Update the plot
        self.ax.clear()
        self.ax.set_title("Latency Over Time")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Latency (ms)")
        self.ax.plot(self.time_data, self.latency_data, color='blue')
        self.ax.set_ylim(0, 1000)
        self.canvas.draw()

# Create the main window and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = LatencyMonitorApp(root)
    root.mainloop()
