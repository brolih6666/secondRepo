from pytube import YouTube
import os
from urllib.error import HTTPError
from socket import timeout
import ssl

# Ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context
current_directory = os.path.dirname(os.path.realpath(__file__))
exe_directory = os.path.dirname(sys.executable)
print(exe_directory)

# Function to read video URLs from a file
def read_video_urls(file_name):
    with open(f"{exe_directory}/{file_name}", 'r') as file:
        urls = file.readlines()
        # Clean up URLs, removing any leading/trailing whitespaces
        urls = [url.strip() for url in urls if url.strip()]
    return urls

# Function to download videos with retry attempts
def download_videos(urls):
    save_path = os.path.join(exe_directory, 'Pobrane')  # Folder named 'Pobrane'
    print(save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for url in urls:
        try_count = 0
        while try_count < 3:  # Retry download up to 3 times
            try:
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()

                video.download(output_path=save_path, filename=f"{yt.title}.mp4")
                print(f"Pobrane: {yt.title}")
                break  # If download succeeds, move to the next URL

            except (HTTPError, timeout, Exception) as e:
                try_count += 1
                if try_count == 3:
                    print(f"Blad pobierania {url}: {e}")
                else:
                    print(f"Proba ponownego pobierania {url}... Proba nr {try_count}")

# Read video URLs from the file
file_name = 'links.txt'  # Update with the correct file name
video_urls = read_video_urls(file_name)

# Call the function with the list of video URLs
download_videos(video_urls)
