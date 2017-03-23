import pattern.PatternBuilder as PB
import random


def _set_colors(colors):
    if colors is None or len(colors) < 5:
        return [c for i in range(5) for c in PB.random_color()]
    return colors

def get_pattern(colorsA=None, colorsB=None, tall=None, tick_period_ms=0):
    colors = [_set_colors(colorsA), _set_colors(colorsB)]
    if tall is None: tall = (random.randint(0, 1) == 1)
    if tick_period_ms <= 0: tick_period_ms = 200

    frames = [None] * 10
    for i in range(10):
        # Mutated, so shift 1 and -1 from last shift (cumulative shift)
        shifted = [PB.shift(1, colors[0]), PB.shift(-1, colors[1])]
        if tall:
            colors = [shifted[i % 2] for i in range(5)]
            frames[i] = PB.build5(colors)
        else:
            colors = [shifted[i % 2] for i in range(3)]
            frames[i] = PB.build3(colors)

    return (frames, tick_period_ms)
