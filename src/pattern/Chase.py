import pattern.PatternBuilder as PB

def get_pattern(tick_period_ms=0, num_frames=-1):
    if tick_period_ms <= 0: tick_period_ms = 50
    num_frames = 120
    num_ch = 120
    
    frames = [None] * num_frames
    frame = [0] * num_ch
    for i in range(num_frames):
        frame[i] = 255
        frames[i] = frame

    return (frames, tick_period_ms)
