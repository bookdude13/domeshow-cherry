import serial
import sys
import os

from output.FileOutput import FileOutput as FileOutput
from output.ConsoleOutput import ConsoleOutput as ConsoleOutput
from output.SerialOutput import SerialOutput as SerialOutput
from output.DmxOutput import DmxOutput as DmxOutput
from output import DMXException, UsbDmxProException
import pattern.Fade as fade
import pattern.Chase as chase
import pattern.FullRandom as full_random
import pattern.Tsunami as tsunami
import pattern.Sarlacc as sarlacc
import pattern.Radar as radar
import pattern.CounterRotatingCircles as ctr_rot_circles
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
pattern_makers = [
    lambda: (full_random.get_pattern(tick_period_ms=user_input.speed), 'Full Random'),
    lambda: (tsunami.get_pattern(tick_period_ms=user_input.speed), 'Tsunami'),
    lambda: (sarlacc.get_pattern(tick_period_ms=user_input.speed), 'Sarlacc'),
    lambda: (radar.get_pattern(tick_period_ms=user_input.speed), 'Radar'),
    lambda: (ctr_rot_circles.get_pattern(tick_period_ms=user_input.speed), 'Counter Rotating Circles'),
    lambda: (beach_ball.get_pattern(tick_period_ms=user_input.speed), 'Beach Ball'),
    lambda: (pulse.get_pattern(tick_period_ms=user_input.speed), 'Pulse'),
    lambda: (spiral.get_pattern(tick_period_ms=user_input.speed), 'Spiral')
]

# These are the pattern makers used for debugging
debug_patterns = [
    lambda: (fade.get_pattern(tick_period_ms=user_input.speed), 'Fade'),
    lambda: (chase.get_pattern(tick_period_ms=user_input.speed), 'Chase')
]

# Try to create all types of players. Some will fail, which is fine.
# This is quick and dirty way to check that the given output string is valid
cp = Player(ConsoleOutput(), pattern_makers)
try:
    fp = Player(FileOutput(user_input.output), pattern_makers)
    dbg_fp = Player(FileOutput(user_input.output), debug_patterns)
except IOError:
    print('Failed to open FileOutput with output "', user_input.output, '"', sep='')

try:
    sp = Player(SerialOutput(user_input.output, baud=57600), pattern_makers)
    dbg_sp = Player(SerialOutput(user_input.output, baud=57600), debug_patterns)
except serial.SerialException:
    print('Failed to open SerialOutput with output "', user_input.output, '"', sep='')

try:
    dp = Player(DmxOutput(user_input.output), pattern_makers)
    dbg_dp = Player(DmxOutput(user_input.output), debug_patterns)
except (DMXException, UsbDmxProException, serial.SerialException):
    print('Failed to open DmxOutput with output "', user_input.output, '"', sep='')
