import random
import pattern.PatternBuilder as PB

def get_pattern(tick_period_ms=0, num_frames=-1):
    if tick_period_ms <= 0: tick_period_ms = 500
    if num_frames < 0: num_frames = random.randint(6, 9)

    frames = [None] * num_frames
    for i in range(num_frames):
    	color = PB.random_color()
    	frames[i] = PB.build5([color] * 5)

    return (frames, tick_period_ms)
