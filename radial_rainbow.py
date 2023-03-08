import inky_frame
import math
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7
graphics = PicoGraphics(DISPLAY_INKY_FRAME_7)

WIDTH, HEIGHT = graphics.get_bounds()

graphics.set_pen(inky_frame.BLACK)
graphics.clear()

r = 200
rays = 360

for i in range(rays):
    graphics.set_pen(graphics.create_pen_hsv(float(i) / rays, 1.0, 1.0))
    a = math.radians(i * 360.0 / rays) + math.pi
    x = math.sin(a) * r
    y = math.cos(a) * r
    x1 = math.sin(a) * (r / 2)
    y1 = math.cos(a) * (r / 2)
    x += WIDTH // 2
    y += HEIGHT // 2
    x1 += WIDTH // 2
    y1 += HEIGHT // 2
    graphics.line(WIDTH // 2, HEIGHT // 2, int(x1), int(y1), 3)
    graphics.line(int(x1), int(y1), int(x), int(y), 6)


graphics.set_pen(inky_frame.WHITE)
graphics.set_thickness(7)
graphics.set_font("cursive")
text_width = graphics.measure_text("Hello World", scale=4)
text_offset_left = (WIDTH - text_width) // 2
graphics.text("Hello World", text_offset_left, HEIGHT // 2, scale=4)

graphics.set_pen(inky_frame.BLACK)
graphics.set_thickness(5)
graphics.text("Hello World", text_offset_left, HEIGHT // 2, scale=4)

graphics.update()
