import time
import gc
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN, PEN_RGB332
from ulab import numpy


# MAXIMUM OVERKILL
# machine.freq(250_000_000)

gu = GalacticUnicorn()
gu.set_brightness(0.5)
graphics = PicoGraphics(DISPLAY_GALACTIC_UNICORN, pen_type=PEN_RGB332)

WIDTH, HEIGHT = graphics.get_bounds()
BYTES_PER_PIXEL = 1  # RGB88 would be four bytes


def update():
    # This is where the magic happens-
    # We copy PicoGraphics buffer into a numpy array of the right dimensions
    buffer = numpy.frombuffer(graphics, dtype=numpy.uint8).reshape((HEIGHT, WIDTH * BYTES_PER_PIXEL))
    # And use `roll` to roll it around like a conveyor belt.
    buffer = numpy.roll(buffer, -BYTES_PER_PIXEL, axis=1)
    # Before copying it back
    memoryview(graphics)[:] = buffer.tobytes()
    # And requesting a display update!
    gu.update(graphics)


t_count = 0
t_total = 0

# Draw something
graphics.set_pen(graphics.create_pen(0, 0, 0))
graphics.clear()

graphics.set_pen(graphics.create_pen(255, 255, 255))
graphics.text("Ohai World", 0, 2, scale=1)

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

    # Don't actually run at peak framerate
    # because it's so fast it's an indistinct blur
    time.sleep(1.0 / 30)
