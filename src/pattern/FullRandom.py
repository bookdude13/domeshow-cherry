import random
import rx
import src.pattern.PatternBuilder as PB

def get_observable(tick_period_ms=0, num_frames=-1):
    if tick_period_ms <= 0: tick_period_ms = random.randint(500, 1200)
    if num_frames < 0: num_frames = random.randint(6, 9)

    # Observable
    return rx.Observable.interval(tick_period_ms) \
        .take(num_frames) \
        .map(lambda i: PB.random_color()) \
        .map(lambda color: PB.build5(color, color, color, color, color))


