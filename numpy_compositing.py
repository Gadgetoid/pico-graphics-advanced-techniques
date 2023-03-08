import time
import gc
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN, PEN_RGB332
from ulab import numpy

# This technique as given only works with RGB332 and P8 surfaces

WIDTH = 53
HEIGHT = 11

# MAXIMUM OVERKILL
# machine.freq(250_000_000)

gu = GalacticUnicorn()
gu.set_brightness(0.5)

# Create numpy arrays to use as buffers for our three PicoGraphics instances
COMPOSITE = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
BACKGROUND = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
FOREGROUND = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)

# Create our three PicoGraphics instances
composite = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332, buffer=COMPOSITE)
bg = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332, buffer=BACKGROUND)
fg = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332, buffer=FOREGROUND)


def update():
    BACKGROUND[:] = numpy.roll(BACKGROUND, -1, axis=1)
    COMPOSITE[:] = numpy.where(FOREGROUND > 0, FOREGROUND, BACKGROUND)
    gu.update(composite)


t_count = 0
t_total = 0

# Draw something in the background layer
for x in range(WIDTH):
    pen = bg.create_pen_hsv(x / WIDTH, 1.0, 1.0)
    bg.set_pen(pen)
    bg.line(x, 0, x, HEIGHT)

# Draw something in the foreground layer
fg.set_pen(0)
fg.clear()
fg.set_pen(255)
fg.text("Score: 10", 1, 0, scale=1)

while True:
    gc.collect()

    tstart = time.ticks_ms()
    update()  # Roll it!
    tfinish = time.ticks_ms()

    total = tfinish - tstart
    t_total += total
    t_count += 1

    if t_count == 60:
        per_frame_avg = t_total / t_count
        print(f"60 frames in {t_total}ms, avg {per_frame_avg:.02f}ms per frame, {1000/per_frame_avg:.02f} FPS")
        t_count = 0
        t_total = 0
