import pattern.PatternBuilder as PB
import random

def get_pattern(color=None, tick_period_ms=0):
    if color is None: color = PB.random_color()
    if tick_period_ms <= 0: tick_period_ms = 200

    frames = [[-1] * 120 for i in range(10)]

    for i in range(10):
        f = frames[i]
        indexes = [i, i + 10, i + 20, (i // 2) + 30, (i // 2) + 35]

        for j in indexes:
            f[ 3*j : 3*(j+1) ] = color
            
    return (frames, tick_period_ms)
