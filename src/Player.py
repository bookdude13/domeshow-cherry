import rx
import random

def _nop(unused = None):
    pass

# This class holds all of the dome's patterns and runs them
class Player:
    """
    Wraps around a stream of PlayerState, where PlayerState is a tagged union
    PlayerState = Live
                | Solid(u8 r, u8 g, u8 b)
                | Pattern(index i)
    Implemented as lists, with variant tag as first index.
    """

    def __init__(self, state_stream):
        self._state_stream = state_stream

    def shutdown(self):
        self._state_stream.on_completed()

    def run_solid(self, r, g, b):
        self._state_stream.on_next(['solid', r, g, b])

    def run_live(self):
        self._state_stream.on_next(['live'])

    def run_pattern(self, i):
        self._state_stream.on_next(['pattern', i])

def make_player(output, pattern_makers):
    """
    Factory for initializing observable graph and subscribing output to a
    player. The output will be closed when the player is shutdown.

    Args:
        output: Output to write to.
        pattern_makers: List of functions taking no args and returning a
            (Observable<[u8]>, info object).
    """

    if len(pattern_makers) == 0:
        raise ValueError('pattern_makers is empty')

    # Switch on state variants
    handle_state = {
        'solid': _make_solid_stream(),
        'live': _make_live_stream(pattern_makers),
        'pattern': _make_pattern_stream(pattern_makers)
    }

    def _passthrough(acc, x):
        for i in range(len(x)):
            if x[i] == -1:
                x[i] = acc[i]
        return x

    state_stream = rx.subjects.Subject()

    # Make data stream and subscribe output to it.
    state_stream \
        .map(lambda state: handle_state[state[0]](state)) \
        .switch_latest() \
        .scan(_passthrough, [0] * 120) \
        .do_action(_bound_data, _nop, _nop) \
        .subscribe(
            on_next = output.send,
            on_error = lambda e: output.close(str(e)),
            on_completed = lambda: output.close('Completed'))
    
    return Player(state_stream)

def _make_solid_stream():
    def stream(state):
        return rx.Observable.just(state[1:4] * 40)

    return stream

def _make_pattern_stream(pattern_makers):
    def stream(state):
        try:
            return pattern_makers[state[1]]()[0]
        except Exception as e:
            print("Pattern maker {} error: {}".format(state[1], e))
            return rx.Observable.empty()

    return stream

def _make_live_stream(pattern_makers):
    log_err = lambda e: print("Pattern maker error: " + str(e))

    def stream(state):
        return rx.Observable.repeat(None) \
            .map(lambda none: random.choice(pattern_makers)) \
            .map(lambda pmaker: pmaker()) \
            .do_action(_nop, log_err, _nop) \
            .retry() \
            .map(_error_handle_sub_stream) \
            .do_action(lambda c: print('New substream'), _nop, _nop) \
            .concat_all()

    return stream

# Ensure that a erroring sub stream completes gracefully        
def _error_handle_sub_stream(args):       
    (sub_stream, info) = args     

    log_err = lambda e: print("Sub stream error: {}, {}".format(info, e))
     
    return sub_stream \
        .do_action(_nop, log_err, _nop) \
        .catch_exception(rx.Observable.empty())

def _bound_data(data):
    for i in range(len(data)):
        data[i] = _bound_datum(data[i])

def _bound_datum(x):
    if x < 0:
        return 0
    elif x > 255:
        return 255
    return x
