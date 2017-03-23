import random
import multiprocessing

class PatternQueue:
    """
    Creates and maintains a queue of patterns that can be run. Uses
    a separate process to keep queue full with prepped patterns.
    """

    # size: number of patterns maintained in the queue
    # patterns: list of pattern makers tuples
    # The format for each pattern maker is (function_to_get_pattern_frames, 'pattern name')
    def __init__(self, size, patterns):
        self._queue = multiprocessing.Queue(size)
        self._patterns = patterns
        self.size = size

        # Initially fill queue with random patterns
        for i in range(self.size):
            self._enqueue_pattern()

        # Create and start another process that will keep queue filled
        self._filler_process = multiprocessing.Process(target=self._keep_queue_filled, name="cherry-filling")
        self._filler_process.start()

    def _keep_queue_filled(self):
        while True:
            self._enqueue_pattern()

    # Adds a random pattern to the queue, blocking if queue is full
    def _enqueue_pattern(self):
        idx = random.randrange(len(self._patterns))
        (pattern, name) = self._patterns[idx]()
        (frames, tick_period_ms) = pattern
        self._queue.put((name, frames, tick_period_ms), block=True)

    # Gets the next pattern from the queue. Blocks if none available.
    # The returned pattern maker is a tuple of the form (pattern_observable, 'pattern name')
    def get(self):
        return self._queue.get(block=True)



