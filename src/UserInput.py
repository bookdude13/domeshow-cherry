import argparse
from output.FileOutput import FileOutput as FileOutput


class UserInput:
    def __init__(self):
        args = self._parse()
        self.output = args.output
        self.speed = args.speed

    # Parse command line arguments
    def _parse(self):
        parser = argparse.ArgumentParser(prog='cherry')
        parser.add_argument(
            '-o',
            '--output',
            default='/tmp/cherrylog')
        parser.add_argument(
            '--speed',
            type=int,
            default=1000)
        return parser.parse_args()


