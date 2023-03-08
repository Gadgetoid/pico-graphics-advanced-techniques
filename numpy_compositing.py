import time
import gc
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN, PEN_RGB332
from ulab import numpy

# This technique as given only works with RGB332 and P8 surfaces
# it *could* work with RGB888 but that would require 4x as much RAM
# and careful consideration not to shift your R, G and B bytes into
# the wrong position.

# The general idea is to give PicoGraphics instances a numpy array
# as their back buffer. Since numpy arrays support the buffer interface
# this Just Works and our PicoGraphics instances get a block of memory
# like we'd expect.

# You can draw using PicoGraphics methods as you normally would.

# The power comes from having this memory also wrapped as a 2d numpy
# array which we can do fancy numpy things with.

# Everything you draw via PicoGraphics can be seen in the `BACKGROUND`
# and `FOREGROUND` buffer arrays.

WIDTH = 53
HEIGHT = 11

# MAXIMUM OVERKILL
# machine.freq(250_000_000)

gu = GalacticUnicorn()
gu.set_brightness(0.5)

# Create numpy arrays to use as buffers for our three PicoGraphics instances
# By creating them as numpy arrays we can manipulate and query them very quickly
# without having to call PicoGraphics drawing methods, or redraw our whole image.
COMPOSITE = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
BACKGROUND = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
FOREGROUND = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)

# Create our three PicoGraphics instances using the numpy arrays as buffers
composite = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332, buffer=COMPOSITE)
bg = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332, buffer=BACKGROUND)
fg = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332, buffer=FOREGROUND)

# Draw something in the background layer
# This will plot a left to right rainbow effect
for x in range(WIDTH):
    pen = bg.create_pen_hsv(x / WIDTH, 1.0, 1.0)
    bg.set_pen(pen)
    bg.line(x, 0, x, HEIGHT)

# Roll each row of our background layer to skew
# the rainbow effect and make it look fancier.
for y in range(HEIGHT):
    BACKGROUND[y] = numpy.roll(BACKGROUND[y], -(y + 1))

# Draw something in the foreground layer
fg.set_pen(0)
fg.clear()
fg.set_pen(255)
fg.text("Score: 10", 1, 0, scale=1)

# Just some variables to keep track of our framerate
t_count = 0
t_total = 0

while True:
    gc.collect()  # Garbage collect every frame so it's evenly paced

    tstart = time.ticks_ms()

    # Roll the background so we can see *something* happening without having to redraw
    # this moves every single pixel left by 1, wrapping the left-most pixels around to the right edge.
    BACKGROUND[:] = numpy.roll(BACKGROUND, -1, axis=1)

    # Now composite the layers together, selecting the foreground pixel if it's non-zero,
    # otherwise filling in with the background.
    COMPOSITE[:] = numpy.where(FOREGROUND > 0, FOREGROUND, BACKGROUND)

    # Finally, update Galactic Unicorn with the result, which ends up in the "composite"
    # PicoGraphics instance, since we've directly altered its buffer.
    gu.update(composite)

    tfinish = time.ticks_ms()

    total = tfinish - tstart
    t_total += total
    t_count += 1

    if t_count == 60:
        per_frame_avg = t_total / t_count
        print(f"60 frames in {t_total}ms, avg {per_frame_avg:.02f}ms per frame, {1000/per_frame_avg:.02f} FPS")
        t_count = 0
        t_total = 0
