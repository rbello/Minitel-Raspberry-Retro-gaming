#!/usr/bin/env python

#@see https://wiki.labomedia.org/index.php/Renaissance_d%27un_Minitel_avec_une_Raspberry_Pi
#@see http://crumpspot.blogspot.fr/2013/05/using-3x4-matrix-keypad-with-raspberry.html

import RPi.GPIO as GPIO
from Adafruit_MCP230xx import Adafruit_MCP230XX

mcp2 = Adafruit_MCP230XX(0x21, 19)

# Configure GPIOs
GPIO.setmode(GPIO.BCM)

gpio = [21, 26, 20, 19, 16, 13, 6, 12, 5, 25, 24, 22, 23, 27, 17, 18, 4, 15]

class keypad(Adafruit_MCP230XX):
    
	# Constants
    INPUT       = 0
    OUTPUT      = 1
    HIGH        = 1
    LOW         = 0
    
	# Minitel 1 RTIC keyboard
    KEYPAD = [
		["Maj. G ", "W", "B", "N", "Maj. D", "V", "C", "X", "?"],
		["Q", "D", "G", "J", "L", "7", "8", "9", "?"],
		["Ctrl", "S", "F", "H", "K", "M", "P", "O", "?"],
		["A", "Z", "E", "R", "T", "Y", "U", "I", "?"],
		["Esc", ",", ".", "\"", ";", "-", ":", "?", "?"],
		["Connexion", "Guide", "Correction", "Suite", "Envoi", "4", "5", "6", "?"],
		["Fnct", "Sommaire", "Annulation", "Retour", "Répétition", "1", "2", "3", "?"],
		["↑", "↓", "←", "→", "CR", "*", "0", "#", "Espace"],
		["", "", "", "", "", "", "", "", ""]
    ]
    
    ROW         = [21, 26, 20, 19, 16, 13, 6, 12, 5]
    COLUMN      = [25, 24, 22, 23, 27, 17, 18, 4, 15]
     
    def __init__(self, address=0x21, num_gpios=8):
         
        self.mcp2 = Adafruit_MCP230XX(address, num_gpios)
         
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            self.mcp2.config(self.COLUMN[j], self.mcp2.OUTPUT)
            self.mcp2.output(self.COLUMN[j], self.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            self.mcp2.config(self.ROW[i], self.mcp2.INPUT)
            self.mcp2.pullup(self.ROW[i], True)
         
        # Scan rows for pushed key/button
        # valid rowVal" should be between 0 and 3 when a key is pressed. Pre-setting it to -1
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = self.mcp2.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is still "return" then no button was pressed and we can exit
        if rowVal == -1:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
            self.mcp2.config(self.COLUMN[j], self.mcp2.INPUT)
         
        # Switch the i-th row found from scan to output
        self.mcp2.config(self.ROW[rowVal], self.mcp2.OUTPUT)
        self.mcp2.output(self.ROW[rowVal], self.HIGH)
         
        # Scan columns for still-pushed key/button
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = self.mcp2.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
         
        if colVal == -1:
            self.exit()
            return
               
        # Return the value of the key pressed
        self.exit()   
        return self.KEYPAD[rowVal][colVal]
             
    def exit(self):
        # Reinitialize all rows and columns as input before exiting
        for i in range(len(self.ROW)):
                self.mcp2.config(self.ROW[i], self.INPUT) 
        for j in range(len(self.COLUMN)):
                self.mcp2.config(self.COLUMN[j], self.INPUT)

kp = keypad()

# Main loop
try:
        while True:
				r = kp.getKey()
				if r == None:
					continue
				print "Key pressed:", r
                #for i in xrange(18):
                        #print "Value of GPIO", gpio[i], "=", data[i]
                        #current = GPIO.input(gpio[i])
                        #if current != data[i]:
                        #        print "Value changed for GPIO", gpio[i], "from", data[i], "to", current
                        #        data[i] = current
						
except:
        GPIO.cleanup()

