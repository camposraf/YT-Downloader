## Standard Video Downloader by Valkyrie Softworks (est. 2024) ##
import os
import re
import yt_dlp
import PySimpleGUI as sg
import threading

# Set the default output directory to the user's Downloads folder
output_directory = os.path.join(os.path.expanduser("~"), "Downloads")

# Regular expression to match progress lines in the log
progress_line = re.compile(r'\[download\]\s*[\d.]+%')

# Custom logger class to handle logging messages to the GUI window
class YTDLogger:
    def __init__(self, window):
        self.window = window
    def debug(self, msg):
        self.window.write_event_value('-LOG-', msg)
    def warning(self, msg):
        self.window.write_event_value('-LOG-', f"WARNING: {msg}")
    def error(self, msg):
        self.window.write_event_value('-LOG-', f"ERROR: {msg}")
    def info(self, msg):
        self.window.write_event_value('-LOG-', f"INFO: {msg}")

# Function to handle progress updates from yt_dlp and update the GUI window
def progress_hook(d, window):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        percent_value = (downloaded / total * 100) if total else 0
        percent_value = min(100.0, max(0.0, percent_value))

        percent_str = f"{percent_value:.2f}%"
        window.write_event_value('-PROGRESS-', percent_value)
        window.write_event_value('-STATUS-', f"Downloading... {percent_str}")
    elif d['status'] == 'finished':
        window.write_event_value('-STATUS-', "Processing...")

# Function to download a YouTube video using yt_dlp and update the GUI window
def download_yt_video(url, window):
    ydl_opts = {
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b',
        'noplaylist': True,
        'paths': {'home': output_directory},
        'progress_hooks': [lambda d: progress_hook(d, window)],
        'logger': YTDLogger(window)
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        window.write_event_value('-DONE-', "Download Complete!")
    except Exception as e:
        window.write_event_value('-STATUS-', f"Error: {e}")

# GUI layout and event loop
sg.theme('DarkBlack')
layout = [
    [sg.Text("Standard Video Downloader")],
    [sg.Input(key="-URL-", size=(50,1)), sg.Button("Download")],
    [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROG-', bar_color=('green', 'gray'))],
    [sg.Text("", key="-STATUS-")],
    [sg.Multiline(size=(60, 10), key="-LOG-", autoscroll=True, disabled=True)]
]

# Create the main window
window = sg.Window("Standard Video Downloader", layout)
last_progress = 0

# Event loop to handle user interactions and update the GUI
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == "Download":
        url = values["-URL-"].strip()
        if url:
            last_progress = 0
            window['-PROG-'].update(0)
            window['-STATUS-'].update("Starting download...")
            window.refresh()
            threading.Thread(target=download_yt_video, args=(url, window), daemon=True).start()
        else:
            window['-STATUS-'].update("Please enter a URL.")

    elif event == '-PROGRESS-':
        last_progress = max(values['-PROGRESS-'], last_progress)
        window['-PROG-'].update(last_progress)

    elif event == '-STATUS-':
        window['-STATUS-'].update(values['-STATUS-'])

    elif event == '-LOG-':
        msg = values['-LOG-']
        if progress_line.search(msg):
            lines = window['-LOG-'].get().split('\n')
            if lines and progress_line.search(lines[-1]):
                lines[-1] = msg
                window['-LOG-'].update('\n'.join(lines))
            else:
                window['-LOG-'].update(msg + "\n", append=True)
        else:
            window['-LOG-'].update(msg + "\n", append=True)

    elif event == '-DONE-':
        window['-STATUS-'].update(values['-DONE-'])
        window['-PROG-'].update(100)

window.close()