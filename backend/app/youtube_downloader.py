from yt_dlp import YoutubeDL
import os
import time

def download_youtube_audio(url: str) -> str:
    try:
        print(f"Attempting to download from URL: {url}")
        
        # Create temp directory if not exists
        temp_dir = "app/temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate output filename
        timestamp = str(int(time.time()))
        filename = f"yt_{timestamp}_%(title)s.%(ext)s"
        output_path = os.path.join(temp_dir, filename)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        # Download the file
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Get the actual output path (with extension)
        actual_output_path = output_path.replace('%(title)s', ydl.extract_info(url, download=False)['title'])
        actual_output_path = actual_output_path.replace('%(ext)s', 'mp3')
        
        print(f"Download completed to: {actual_output_path}")
        return actual_output_path
        
    except Exception as e:
        print(f"Detailed error in download_youtube_audio: {str(e)}")
        raise RuntimeError(f"YouTube download failed: {str(e)}")