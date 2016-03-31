import argparse


class UserInput:
    def __init__(self):
        self._output = '/dev/null'
        self._parse()

    def get_output(self):
        return self._output

    # Return True if dev exists
    # TODO implement
    def _valid_device(self, dev):
        return dev

    # Parse command line arguments
    def _parse(self):
        parser = argparse.ArgumentParser(prog='./Cherry.py')
        parser.add_argument('-o', '--output', default='/dev/null', type=self._valid_device)
        args = parser.parse_args()
        self._output = args.output


