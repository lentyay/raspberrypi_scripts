#!/usr/bin/python

# ===========================================================================
# Shut Down or Reset button for Raspberry Pi B+ (40 GPIO pins)              #
# Requires PiGlow Python class                                              #
# https://github.com/Boeeerb/PiGlow                                         #
# ===========================================================================

# Import the libraries to use time delays, send os commands and access GPIO pins
from piglow import PiGlow
from time import sleep

piglow = PiGlow()

ledbrightness = 3 # LED brightness
step = 6 # Count of steps (3 for arms or 6 for colors)

piglow.all(0)

while True:
    piglow.all(0)
    piglow.colour(step,ledbrightness)
    step -= 1
    if step == 0:
        step = 6
    sleep(1)

