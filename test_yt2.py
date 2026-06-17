import yt_dlp
import asyncio

def get_song_info():
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extractor_args': {'youtube': ['player_client=ios,android,web']}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info('ytsearch1:hindia secukupnya', download=False)['entries'][0]['title']

async def main():
    loop = asyncio.get_running_loop()
    title = await loop.run_in_executor(None, get_song_info)
    print(title)

if __name__ == '__main__':
    asyncio.run(main())
