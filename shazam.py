#!/usr/bin/env python
import asyncio
from shazamio import Shazam
from samplebase import SampleBase
from rgbmatrix import graphics
import time

# Global variables to store Shazam data
song_title = ""
artist = ""
album = ""
album_cover_art_link = ""

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="")

    def run(self):
        global song_title, artist, album, album_cover_art_link
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/6x10.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width

        # Combine the text to display all variables
        song_label = f"Song: {song_title}"
        artist_label = f"Artist: {artist}"
        album_label = f"Album: {album}"

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, song_label)
            graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, artist_label)
            graphics.DrawText(offscreen_canvas, font, pos, 30, textColor, album_label)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

async def find():
    global song_title, artist, album, album_cover_art_link
    
    shazam = Shazam()
    data = await shazam.recognize('always_forever.mp3')  # Update the file path if necessary

    # Extracting the information
    song_title = data['track']['title']
    artist = data['track']['subtitle']
    album = data['track']['sections'][0]['metadata'][0]['text']
    album_cover_art_link = data['track']['images']['coverart']

    print(f"Song title: {song_title}\nArtist: {artist}\nAlbum: {album}\nAlbum Cover Link: {album_cover_art_link}\n")

if __name__ == "__main__":
    # Run the Shazam recognition to set global variables
    loop = asyncio.get_event_loop()
    loop.run_until_complete(find())

    # Create and run the RunText instance
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
