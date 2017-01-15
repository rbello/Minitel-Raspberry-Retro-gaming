#!/bin/python

import smbus
from time import sleep
import sys
import os
import subprocess

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

# Write a value to start conversation
bus.write_byte(address, 0)

oldVolume = 0

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
			volume = 0.0
			if code <= 10:
				volume = 0.0
			else:
				volume = 39.0 + (code / 100.0) * 60.0
			move = ") +" if volume > oldVolume else ") -"
			oldVolume = volume
			print('Volume: ' + str(code) + '% (' + str(int(volume)) + move)
			try:
				subprocess.call(["amixer", "sset", "PCM", str(int(volume)) + "%"], stdout=subprocess.PIPE)
			except BaseException as ex:
				print('Error setting volume', ex)
		elif code == 200:
			print('Shutdown!')
			os.system('shutdown now -h')
			break
		else:
			print('Invalid code: ', code)
except BaseException as e:
        print('Exit: ', e)

bus.close()
sys.exit()
