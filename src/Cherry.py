import serial
import sys
import os

from output.FileOutput import FileOutput as FileOutput
from output.ConsoleOutput import ConsoleOutput as ConsoleOutput
from output.SerialOutput import SerialOutput as SerialOutput
from output.DmxOutput import DmxOutput as DmxOutput
from output import DMXException, UsbDmxProException
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
pattern_makers = [
    lambda: (full_random.get_observable(tick_period_ms=user_input.speed), 'Full Random'),
    lambda: (tsunami.get_observable(tick_period_ms=user_input.speed), 'Tsunami'),
    lambda: (sarlacc.get_observable(tick_period_ms=user_input.speed), 'Sarlacc'),
    lambda: (radar.get_observable(tick_period_ms=user_input.speed), 'Radar'),
    lambda: (crc.get_observable(tick_period_ms=user_input.speed), 'Counter Rotating Circles'),
    lambda: (beach_ball.get_observable(tick_period_ms=user_input.speed), 'Beach Ball'),
    lambda: (pulse.get_observable(tick_period_ms=user_input.speed), 'Pulse'),
    lambda: (spiral.get_observable(tick_period_ms=user_input.speed), 'Spiral')
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
except serial.SerialException:
    print('Failed to open SerialOutput with output "', user_input.output, '"', sep='')

try:
    dp = Player(DmxOutput(user_input.output), pattern_makers)
except (DMXException, UsbDmxProException, serial.SerialException):
    print('Failed to open DmxOutput with output "', user_input.output, '"', sep='')
