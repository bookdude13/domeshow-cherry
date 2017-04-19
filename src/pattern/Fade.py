import colorsys
import pattern.PatternBuilder as PB

def get_pattern(tick_period_ms=0, num_frames=360):
    if tick_period_ms <= 0: tick_period_ms = 50
    if num_frames < 0: num_frames = 360

    frames = [None] * num_frames
    for i in range(num_frames):
        color = 255 * colorsys.hsv_to_rgb(i / num_frames, 1, 1)
        frames[i] = PB.build5([color] * 5)

    return (frames, tick_period_ms)
