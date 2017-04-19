import rx
import random

from PatternQueue import PatternQueue

# This class holds all of the dome's patterns and runs them
class Player:
    """
    Handles the running of dome patterns. These can be either solid
    colors (run_solid), patterns (run_pattern), or a continuous
    stream of patterns (run_live).
    """

    def __init__(self, output, pattern_makers):
        self._output = output
        self._pattern_queue = PatternQueue(5, pattern_makers)
        self._pattern_makers = pattern_makers

    # Convenience function to turn all lights off
    # Identical to run_solid(0, 0, 0)
    def off(self):
        self.run_solid(0, 0, 0)

    # Convenience function to turn all lights on
    # Identical to run_solid(255, 255, 255)
    def on(self):
        self.run_solid(255, 255, 255)

    # Makes the entire dome one color
    def run_solid(self, r, g, b):
        frame = [r, g, b] * 40
        self._output.send(frame)

    # Continuously run randomly selected patterns
    def run_live(self):
        # Get a random pattern
        (name, pattern_frames, tick_period_ms) = self._pattern_queue.get()
        
        # Once a pattern finishes, inform the user and run again
        def _pattern_done():
            print('Pattern {} completed'.format(name))
            self.run_live()

        # Create pattern stream
        pattern_stream = rx.Observable.interval(tick_period_ms) \
            .take(len(pattern_frames)) \
            .map(lambda i: pattern_frames[i])

        # Run the pattern
        pattern_stream \
            .scan(_passthrough, [0] * 120) \
            .do_action(_bound_data, _nop, _nop) \
            .subscribe(
                on_next = self._output.send,
                on_error = lambda e: self._output.close(str(e)),
                on_completed = _pattern_done)

    # Get a pattern by index and run it
    def run_pattern(self, i):
        # Check that the index is valid
        if i < 0 or i >= len(self._pattern_makers):
            raise ValueError("Invalid pattern - out of range")
        
        # Get the pattern
        (pattern, name) = self._pattern_makers[i]()
        (pattern_frames, tick_period_ms) = pattern

        # Create pattern stream
        pattern_stream = rx.Observable.interval(tick_period_ms) \
            .take(len(pattern_frames)) \
            .map(lambda i: pattern_frames[i])

        # Run the pattern
        pattern_stream \
            .scan(_passthrough, [0] * 120) \
            .do_action(_bound_data, _nop, _nop) \
            .subscribe(
                on_next = self._output.send,
                on_error = lambda e: self._output.close(str(e)),
                on_completed = lambda: print('Pattern {} completed'.format(info)))


# Function that does nothing (used for Rx observables)
def _nop(unused = None):
    pass

# Takes a list of frame data and maps all '-1's to the last
# frame's data (passes through, acts transparent) 
def _passthrough(accumulated, x):
    for i in range(len(x)):
        if x[i] == -1:
            x[i] = accumulated[i]
    return x

# Makes sure all elements of data have their range bound by _bound_datum
def _bound_data(data):
    for i in range(len(data)):
        data[i] = _bound_datum(data[i])

# Maps value to range [0, 255]. If smaller, set to minimum. If bigger,
# set to maximum
def _bound_datum(x):
    if x < 0:
        return 0
    elif x > 255:
        return 255
    return x
