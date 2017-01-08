#!/bin/python

import RPi.GPIO as gpio
import smbus
from time import sleep
import sys
import os

# I2C
bus = smbus.SMBus(1)    # # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C$
address = 0x04          # 7 bit address

# GPIO
#gpio.setmode(gpio.BCM)
#gpio.setup(4, gpio.OUT, initial=gpio.HIGH)
#gpio.output(4, gpio.HIGH)
#print('GPIO signal RUNNING set to TRUE')

# Send to arduino
def writeNumber(value):
        bus.write_byte(address, int(value))
        return -1

# Read from arduino
def readNumber():
        number = bus.read_byte(address)
        return number

print('Polling I2C...')

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
                        #os.system('shutdown now -h')
                        break
                else:
                        print('Invalid code: ', code)
except Exception as e:
        print('Exit: ', e)

bus.close()
#gpio.cleanup()
sys.exit()
