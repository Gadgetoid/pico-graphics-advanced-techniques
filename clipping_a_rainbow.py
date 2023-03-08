import time
import inky_frame
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7

TEXT = "Hello World, how are you?"

graphics = PicoGraphics(DISPLAY_INKY_FRAME_7)
WIDTH, HEIGHT = graphics.get_bounds()

graphics.set_pen(inky_frame.BLACK)
graphics.clear()

graphics.set_font("cursive")

rows = 6
row_height = (HEIGHT - 60) // rows

t_start = time.ticks_ms()

# Do this in 20 pixel wide "scanlines" since doing it
# at "full resolution" takes about 50 seconds and
# this doesn't really look any different.
# As it is, this takes ~3s to render.
SCANLINE_WIDTH = 20
SCANLINES = WIDTH // SCANLINE_WIDTH

# Okay we're going to render our six lines of text
# WIDTH / SCANLINE_WIDTH times, which is 40 passes
# on the 800x480 pixel Inky Frame 7.3"
# For each pass we'll set the clipping region so that
# only a portion of the text gets rendered.
# We'll also set its colour so we get a left/right rainbow.
for x in range(SCANLINES):
    graphics.set_clip(x * SCANLINE_WIDTH, 0, SCANLINE_WIDTH, HEIGHT)
    # Create our rainbow pen using x as the hue.
    graphics.set_pen(graphics.create_pen_hsv(x / SCANLINES, 1.0, 1.0))

    for i in range(rows):
        x_offset = 30
        y_offset = i * row_height + (row_height // 2) + 30

        # Rainbow text
        graphics.set_thickness(i + 1)
        graphics.text(TEXT, x_offset, y_offset, scale=2)

t_end = time.ticks_ms()

print(f"Woof! Rendering took {t_end - t_start}ms.")

graphics.update()
