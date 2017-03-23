import pattern.PatternBuilder as PB
import random

def get_pattern(color=None, tick_period_ms=0):
    if color is None: color = PB.random_color()
    if tick_period_ms <= 0: tick_period_ms = 50

    frames = [[-1] * 120 for i in range(40)]

    for i in range(40):
        frames[i][i*3:(i+1)*3] = color

    return (frames, tick_period_ms)
