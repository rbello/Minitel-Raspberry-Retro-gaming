#!/usr/bin/python
import RPi.GPIO as gpio
import os

#Set pin numbering to BCM numbering
gpio.setmode(gpio.BCM)

#Set up pin as an input
gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# Set up an interrupt to look for pressed button
gpio.wait_for_edge(18, gpio.FALLING)

# Shutdown
#os.system('shutdown now -h')
print('Shutdown signal received')