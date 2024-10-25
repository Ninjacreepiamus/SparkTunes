import asyncio
from shazamio import Shazam


async def main():
    shazam = Shazam()
    # out = await shazam.recognize_song('dora.ogg') # slow and deprecated, don't use this!
    data = await shazam.recognize('always_forever.mp3')  # rust version, use this!

    # Extracting the information
    song_title = data['track']['title']
    artist = data['track']['subtitle']
    album = data['track']['sections'][0]['metadata'][0]['text']
    album_cover_art_link = data['track']['images']['coverart']

    print(f"Song title: {song_title}\nArtist: {artist}\nAlbum: {album}\nAlbum Cover Link:{album_cover_art_link}\n")



loop = asyncio.get_event_loop()
loop.run_until_complete(main())