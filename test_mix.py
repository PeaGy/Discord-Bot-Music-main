import yt_dlp
import json
import random

url = "https://www.youtube.com/watch?v=kJQP7kiw5Fk&list=RDkJQP7kiw5Fk"
ydl_opts = {
    "extract_flat": True,
    "quiet": True,
    "playlist_end": 10
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    entries = info.get("entries", [])
    valid_entries = [e for e in entries if e.get("id") != "kJQP7kiw5Fk"]
    if valid_entries:
        picked = random.choice(valid_entries[:5])
        print(json.dumps(picked, indent=2))
    else:
        print("No entries")
