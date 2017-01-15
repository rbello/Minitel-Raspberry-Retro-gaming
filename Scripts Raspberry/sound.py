#!/bin/python

import smbus
from time import sleep
import sys
import os
import pygame
from subprocess import call
#import alsaaudio

# I2C
bus = smbus.SMBus(1)	# # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
address = 0x04		# 7 bit address

# Send to arduino
def writeNumber(value):
	bus.write_byte(address, int(value))
	return -1

# Read from arduino
def readNumber():
	number = bus.read_byte(address)
	return number

print('Polling I2C...')

# Volume : 100%
call(["amixer", "-D", "pulse", "sset", "Master", "100%"])
#m = alsaaudio.Mixer(alsaaudio.mixers[0])
#m.setvolume(90)
# Play a startup sound
#pygame.mixer.init()
#pygame.mixer.music.load("welcome.wav")
#pygame.mixer.music.play()
#while pygame.mixer.music.get_busy() == True:
#    continue

# Write a value to start conversation
bus.write_byte(address, 0)

try:
        while True:
                try:
                        data = bus.read_byte(address)
                except IOError:
                        sleep(1)
                        continue
                # Rien a se dire
                if data == 0:
                        sleep(0.2)
                        continue
		code = int(data)
		if code > 0 and code <= 100:
			print('Volume: ', code)
		elif code == 200:
			print('Shutdown!')
			os.system('shutdown now -h')
			break
		else:
			print('Invalid code: ', code)
except Exception as e:
        print('Exit: ', e)

bus.close()
sys.exit()
