import src.pattern.PatternBuilder as PB
import random
from rx import Observable

def get_observable(color=None, offset=0, tick_period_ms=0):
    if color is None: color = PB.random_color()
    if tick_period_ms <= 0: tick_period_ms = 200

    last = [-1, -1, -1]

    layer_sets = [(i * [last]) + [color] + ((9-i) * [last]) for i in range(10)]
    frames = [PB.build10(layers, offset) for layers in layer_sets]

    return Observable.interval(tick_period_ms) \
        .take(10) \
        .map(lambda i: frames[i])
