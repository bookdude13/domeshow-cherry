import pattern.PatternBuilder as PB
import random

def get_pattern(color=None, offset=0, tick_period_ms=0):
    if color is None: color = PB.random_color()
    if tick_period_ms <= 0: tick_period_ms = 200

    last = [-1, -1, -1]

    layer_sets = [(i * [last]) + [color] + ((9-i) * [last]) for i in range(10)]
    unordered_frames = [PB.build10(layers, offset) for layers in layer_sets]

    frames = \
        [unordered_frames[i] for i in range(0, 9, 2)] + \
        [unordered_frames[i] for i in range(9, 0, -2)]

    return (frames, tick_period_ms)
