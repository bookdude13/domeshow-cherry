import sys
import os

from output.FileOutput import FileOutput as FileOutput
from output.ConsoleOutput import ConsoleOutput as ConsoleOutput
from output.SerialOutput import SerialOutput as SerialOutput
from output.DmxOutput import DmxOutput as DmxOutput
import pattern.FullRandom as full_random
import pattern.Tsunami as tsunami
import pattern.Sarlacc as sarlacc
import pattern.Radar as radar
import pattern.CounterRotatingCircles as crc
import pattern.BeachBall as beach_ball
import pattern.Pulse as pulse
import pattern.Spiral as spiral
from Player import Player
from UserInput import UserInput

user_input = UserInput()

# This is all pattern makers used when running a live stream
# of patterns. They are kept as promises to reduce unnecessary
# allocations, as well as to guarantee different versions of
# each pattern on every call.
# The format for each pattern maker is (pattern_observable, 'pattern name')
user_speed = int(user_input.speed)
pattern_makers = [
    lambda: (full_random.get_pattern(tick_period_ms=user_speed), 'Full Random'),
    lambda: (tsunami.get_pattern(tick_period_ms=user_speed), 'Tsunami'),
    lambda: (sarlacc.get_pattern(tick_period_ms=user_speed), 'Sarlacc'),
    lambda: (radar.get_pattern(tick_period_ms=user_speed), 'Radar'),
    lambda: (crc.get_pattern(tick_period_ms=user_speed), 'Counter Rotating Circles'),
    lambda: (beach_ball.get_pattern(tick_period_ms=user_speed), 'Beach Ball'),
    lambda: (pulse.get_pattern(tick_period_ms=user_speed), 'Pulse'),
    lambda: (spiral.get_pattern(tick_period_ms=user_speed), 'Spiral')
]

# Try to create all types of players. Some will fail, which is fine.
# This is quick and dirty way to check that the given output string is valid
cp = Player(ConsoleOutput(), pattern_makers)
try:
    fp = Player(FileOutput(user_input.output), pattern_makers)
except IOError:
    print('Failed to open FileOutput with output "', user_input.output, '"', sep='')

try:
    sp = Player(SerialOutput(user_input.output), pattern_makers)
except Exception:
    print('Failed to open SerialOutput with output "', user_input.output, '"', sep='')

try:
    dp = Player.make_player(DmxOutput(user_input.output), pattern_makers)
except Exception:
    print('Failed to open DmxOutput with output "', user_input.output, '"', sep='')
