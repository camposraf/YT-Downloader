import yt_dlp 

#Selecting filepath
output_directory = r'C:\Users\Home\Downloads'

def download_yt_video(url):
    ydl_opts ={
        'format' : 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
        'noplaylist' : True,
        'paths' : {'home': output_directory}
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    while True:
        print("Youtube Downloader by Valkyrie Softworks")
        video_url = input("Enter Link: ")
    
        download_yt_video(video_url)
