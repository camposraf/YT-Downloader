import yt_dlp 
import PySimpleGUI as sg
import threading

# Selecting filepath
output_directory = r'C:\Users\Home\Downloads'

# Custom Logger to capture yt-dlp output
class YTDLogger:
    def __init__(self, window):
        self.window = window
    def debug(self, msg):
        self.window.write_event_value('-LOG-', msg)
    def warning(self, msg):
        self.window.write_event_value('-LOG-', f"WARNING: {msg}")
    def info(self, msg):
        self.window.write_event_value('-LOG-', f"INFO: {msg}")

# Progress Bar
def progress_hook(d, window):
    if d['status'] == 'downloading':
        # Use raw numbers for accuracy
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        percent_value = downloaded / total * 100

        percent_str = f"{percent_value:.2f}%"
        window.write_event_value('-PROGRESS-', percent_value)
        window.write_event_value('-STATUS-', f"Downloading... {percent_str}")
        window.write_event_value('-LOG-', d.get('info_dict', {}).get('title', ''))

    elif d['status'] == 'finished':
        window.write_event_value('-STATUS-', "Processing...")

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

# Window Design
layout = [
    [sg.Text("YouTube Downloader")],
    [sg.Input(key="-URL-", size=(50,1)), sg.Button("Download")],
    [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROG-')],
    [sg.Text("", key="-STATUS-")],
    [sg.Multiline(size=(60, 10), key="-LOG-", autoscroll=True ,disabled=True)]
]

window = sg.Window("YT Downloader by Valkyrie Softworks", layout)

# Event Loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Download":
        url = values["-URL-"].strip()
        if url:
            window['-PROG-'].update(0)
            window['-STATUS-'].update("Starting download...")
            window.refresh()

            threading.Thread(
                    target=download_yt_video,
                    args=(url, window),
                    daemon=True
                    ).start()
        else:
            window['-STATUS-'].update("Please enter a URL.")

    elif event == '-PROGRESS-':
        window['-PROG-'].update(values['-PROGRESS-'])
    
    elif event == '-STATUS-':
        window['-STATUS-'].update(values['-STATUS-'])

    elif event == '-LOG-':
        window['-LOG-'].update(values['-LOG-'] + "\n", append=True)

    elif event == '-DONE-':
        window['-STATUS-'].update(values['-DONE-'])
        window['-PROG-'].update(100)
    
window.close()

