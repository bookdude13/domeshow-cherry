import pattern.PatternBuilder as PB
import random

# Pulse layer by layer, up or down
def get_pattern(
        color=None,
        reverse_pattern=None, # boolean
        tall=None, # boolean
        tick_period_ms=0):

    if color is None: color = PB.random_color()
    if reverse_pattern is None: reverse_pattern = (random.randint(0, 1) == 1)
    if tall is None: tall = (random.randint(0, 1) == 1)
    if tick_period_ms <= 0: tick_period_ms = 200

    last = [-1, -1, -1]

    if tall:
        layer_sets = [(i * [last]) + [color] + ((4-i) * [last]) for i in range(5)]
        frames = [PB.build5(layers) for layers in layer_sets]
    else:
        layer_sets = [(i * [last]) + [color] + ((2-i) * [last]) for i in range(3)]
        frames = [PB.build3(layers) for layers in layer_sets]

    if reverse_pattern:
        frames = frames[::-1]

    return (frames, tick_period_ms)
