#!/usr/bin/env python

#    _________                          _________                        
#   /   _____/__ ________   ___________/   _____/_  _  _______     ____  
#   \_____  \|  |  \____ \_/ __ \_  __ \_____  \\ \/ \/ /\__  \   / ___\ 
#   /        \  |  /  |_> >  ___/|  | \/        \\     /  / __ \_/ /_/  >
#  /_______  /____/|   __/ \___  >__| /_______  / \/\_/  (____  /\___  / 
#          \/      |__|        \/             \/              \//_____/  
#
# This file is a part of the SuperSwag projet.
# Copyleft 2017 - evolya.fr
#
#@see https://wiki.labomedia.org/index.php/Renaissance_d%27un_Minitel_avec_une_Raspberry_Pi
#@see http://crumpspot.blogspot.fr/2013/05/using-3x4-matrix-keypad-with-raspberry.html

import RPi.GPIO as GPIO

class keypad():
    
	# Minitel 1 RTIC keyboard
	KEYPAD = [
		["Q", "D", "G", "J", "L", "7", "8", "9", "?"],
		["Maj. G", "W", "B", "N", "Maj. D", "V", "C", "X", "?"],
		["Ctrl", "S", "F", "H", "K", "M", "P", "O", "?"],
		["A", "Z", "E", "R", "T", "Y", "U", "I", "?"],
		["Esc", ",", ".", "'", ";", "-", ":", "?", "?"],
		["Connexion", "Guide", "Correction", "Suite", "Envoi", "4", "5", "6", "?"],
		["Fnct", "Sommaire", "Annulation", "Retour", "Repetition", "1", "2", "3", "?"],
		["Up", "Down", "Left", "Right", "CR", "*", "0", "#", "Espace"],
		["", "", "", "", "", "", "", "", ""]
    ]
    
    ROW         = [21, 26, 20, 19, 16, 13, 6, 12, 5]
    COLUMN      = [25, 24, 22, 23, 27, 17, 18, 4, 15]
     
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
         
    def getKey(self):
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Scan rows for pushed key/button
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal >= len(self.ROW):
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal >= len(self.COLUMN):
            self.exit()
            return
 
        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]

    def exit(self):
        # Reinitialize all rows and columns as input before exiting
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

kp = keypad()

pressed = []

# Main loop
try:
        while True:
		r = kp.getKey()
		if r == None:
			if pressed:
				for key in pressed:
					print "Key released:", key
				pressed = []
			continue
		if r in pressed:
			continue
		print "Key pressed:", r
		pressed.append(r)
except:
        GPIO.cleanup()
