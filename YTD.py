import yt_dlp 
import PySimpleGUI as sg

# Selecting filepath
output_directory = r'C:\Users\Home\Downloads'

def download_yt_video(url):
    ydl_opts ={
        'format' : 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
        'noplaylist' : True,
        'paths' : {'home': output_directory},
        'logger': None,
        'verbose': True
    }

    try: 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download Complete!"
    except Exception as e:
        return f"Error: {e}"
    
# Window Design
layout = [
    [sg.Text("Please enter link: ")], 
    [sg.InputText(key="-URL-", size=(50,1)), sg.Button('Download'), sg.Button('Cancel')], 
    [sg.Text("", key="-STATUS-")]
    ]

window = sg.Window("YT Downloader by Valkyrie Softworks", layout)

# Event Loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Download":
        url = values ["-URL-"].strip()
        if url:
            window["-STATUS-"].update("Downloading...")
            window.refresh()
            
            result = download_yt_video(url)
            window["-STATUS-"].update(result)
        else: 
            window["-STATUS-"].update("Please enter link: ")

window.close()

