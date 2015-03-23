#!/usr/bin/python

# ===========================================================================
# Shut Down or Reset button for Raspberry Pi B+ (40 GPIO pins)              #
# Requires RPi.GPIO Python class                                            #
# https://pypi.python.org/pypi/RPi.GPIO                                     #
#                                                                           #
# Used pins marked with star (*):                                           #
#                                                              *  *         #
#        2  4  6  8  10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40        #
#        |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |         #
#        ----------------------------------------------------------         #
#        |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |         #
#        1  3  5  7  9  11 13 15 17 19 21 23 25 27 29 31 33 35 37 39        #
#                                                                           #
# ===========================================================================

# Import the libraries to use time delays, send os commands and access GPIO pins
import RPi.GPIO as GPIO
from time import sleep
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  # Turn off warnings output
GPIO.setup(38, GPIO.OUT) # Set pin #38 (GPIO20) to output
GPIO.setup(40, GPIO.IN)  # Set pin #40 (GPIO21) to input

while True:
    buttonIn = GPIO.input(40)
    if buttonIn == True:
        print 'System shuts down'
        GPIO.cleanup()
        #os.system("sudo reboot")
        os.system("sudo shutdown -h now")
        break
    sleep(1)
