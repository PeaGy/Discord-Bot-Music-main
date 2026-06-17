import yt_dlp
import sys

ydl_opts = {
    "format": "bestaudio/best",
    "quiet": False,
    "noplaylist": True,
}
url = "http://radio.plaza.one/mp3"
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        info = ydl.extract_info(url, download=False)
        print("Success!", info.get("url"))
    except Exception as e:
        print("Error:", e)
