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
import uinput
import os
import time

class keypad():

	# Minitel 1 RTIC keyboard (text)
	KEYNAME = [
		["Caps L",     "W",       "B",           "N",    "Caps R", "V",     "C",     "X",     "[0x8]"],
		["Q",          "D",       "G",           "J",    "L",      "7",     "8",     "9",     "[1x8]"],
		["Ctrl",       "S",       "F",           "H",    "K",      "M",     "P",     "O",     "[2x8]"],
		["A",          "Z",       "E",           "R",    "T",      "Y",     "U",     "I",     "[3x8]"],
		["Esc",        ",",       ".",           "'",    ";",      "-",     ":",     "?",     "[4x8]"],
		["Connection", "Guide",   "Correction", "Next",  "Send",   "4",     "5",     "6",     "[5x8]"],
		["Fnct",       "Summary", "Cancel",     "Back",  "Repeat", "1",     "2",     "3",     "[6x8]"],
		["Up",         "Down",    "Left",       "Right", "Enter",  "*",     "0",     "#",     "Space"],
		["[8x0]",      "[8x1]",   "[8x2]",      "[8x3]", "[8x4]",  "[8x5]", "[8x6]", "[8x7]", "[8x8]"]
	]

	ALLOW_COMBINE = ["Caps L", "Caps R", "Fnct", "Ctrl"]
	
	# Minitel 1 RTIC keyboard (uinput)
	KEYPAD = [
		[uinput.KEY_LEFTSHIFT,  uinput.KEY_W,      uinput.KEY_B,          uinput.KEY_N,           uinput.KEY_RIGHTSHIFT,  uinput.KEY_V,           uinput.KEY_C,      uinput.KEY_X,         None],
		[uinput.KEY_Q,          uinput.KEY_D,      uinput.KEY_G,          uinput.KEY_J,           uinput.KEY_L,           uinput.KEY_7,           uinput.KEY_8,      uinput.KEY_9,         None],
		[uinput.KEY_LEFTCTRL,   uinput.KEY_S,      uinput.KEY_F,          uinput.KEY_H,           uinput.KEY_K,           uinput.KEY_M,           uinput.KEY_P,      uinput.KEY_O,         None],
		[uinput.KEY_A,          uinput.KEY_Z,      uinput.KEY_E,          uinput.KEY_R,           uinput.KEY_T,           uinput.KEY_Y,           uinput.KEY_U,      uinput.KEY_I,         None],
		[uinput.KEY_ESC,        uinput.KEY_COMMA,  uinput.KEY_DOT,        uinput.KEY_APOSTROPHE,  uinput.KEY_SEMICOLON,   uinput.KEY_MINUS,       uinput.KEY_TAB,    uinput.KEY_QUESTION,  None], # Todo deux-points (tab)
		[uinput.KEY_CONNECT,    uinput.KEY_HELP,   uinput.KEY_BACKSPACE,  uinput.KEY_NEXT,        uinput.KEY_SEND,        uinput.KEY_4,           uinput.KEY_5,      uinput.KEY_6,         None],
		[uinput.KEY_FN,         uinput.KEY_LIST,   uinput.KEY_CANCEL,     uinput.KEY_BACK,        uinput.KEY_REDO,        uinput.KEY_1,           uinput.KEY_2,      uinput.KEY_3,         None],
		[uinput.KEY_UP,         uinput.KEY_DOWN,   uinput.KEY_LEFT,       uinput.KEY_RIGHT,       uinput.KEY_ENTER,       uinput.KEY_KPASTERISK,  uinput.KEY_0,      uinput.KEY_TAB,       uinput.KEY_SPACE], # Todo diese (tab)
		[None,                  None,              None,                  None,                   None,                   None,                   None,              None,                 None]
	]

	# My own attached pins
	ROW         = [26, 21, 20, 19, 16, 13,  6, 12, 5]
	COLUMN      = [25, 24, 22, 23, 27, 17, 18, 4, 14]

	# Virtual keyboard device for uinput
	DEVICE      = None

	# Extra keys
	extraKeys = []
	
	# Observers
	observers = []

	def start(self):
		# Configure GPIO designation model
		GPIO.setmode(GPIO.BCM)
		# Map input keys
		map = []
		for row in self.KEYPAD:
			for key in row:
				if key is not None:
					map.append(key)
		for key in self.extraKeys:
			map.append(key)
		self.DEVICE = uinput.Device(map)

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
				 
		# if rowVal is not set then no button was pressed and we can exit
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
				
		# if colVal is not set then no button was pressed and we can exit
		if colVal < 0 or colVal >= len(self.COLUMN):
			self.exit()
			return
 
		# Return the value of the key pressed
		self.exit()
		#return self.KEYPAD[rowVal][colVal]
		return [rowVal, colVal]

	def exit(self):
		# Reinitialize all rows and columns as input before exiting
		for i in range(len(self.ROW)):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
		for j in range(len(self.COLUMN)):
			GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def addObserver(self, functionName):
		func = globals()[str(functionName)]
		if func not in self.observers:
			self.observers.append(func)

	def notifyObservers(self, event, keyName, keyCode):
		result = None
		for obs in self.observers:
			r = obs(event, keyName, keyCode)
			if r is not None and result is None:
				result = r
		return result
			
	def onKeyPress(self, keyName, keyCode):
		replace = self.notifyObservers("keyPress", keyName, keyCode)
		if replace is not None:
			print "Replace key press:", keyName, keyCode, "by", replace
			if isinstance(replace, list):
				self.DEVICE.emit_combo(replace)
			else:
				self.DEVICE.emit_click(replace)
		else:
			print "Key press:", keyName
			self.DEVICE.emit_click(keyCode)

	def onKeyComboPress(self, keyName1, keyCode1, keyName2, keyCode2):
		replace = self.notifyObservers("keyComboPress", [keyName1, keyName2], [keyCode1, keyCode2])
		if replace is not None:
			print "Replace keys press:", keyName1, "+", keyName2, [keyCode1, keyCode2], "by", replace
			if isinstance(replace, list):
				kp.DEVICE.emit_combo(replace)
			else:
				self.DEVICE.emit_click(replace)
		else:
			print "Keys press:", keyName1, "+", keyName2
			kp.DEVICE.emit_combo([keyCode1, keyCode2])
	
	def onKeyRelease(self, keyName, keyCode):
		print "Key release:", keyName
		
	def onKeyComboRelease(self, keyName1, keyCode1, keyName2, keyCode2):
		print "Keys release:", keyName1, "+", keyName2
		
	def addExtraKey(self, key):
		if isinstance(key, list):
			self.extraKeys.extend(key)
		else:
			self.extraKeys.append(key)

# Keyboard modifier
runEmulationStation = True;
def AzertyMinitelConverter(event, keyName, keyCode):
	name = keyName[0] + " + " + keyName[1] if isinstance(keyName, list) else keyName
	#print "Convert", name
	if (name == "Connection"):
		print "REBOOT NOW !"
		os.system("sudo reboot")
		return
	return {
	
		# Replace functions keys
		"Summary": uinput.KEY_F4,
		"Guide": uinput.KEY_TAB,
		"Cancel": [uinput.KEY_LEFTCTRL, uinput.KEY_X],
		"Back": [uinput.KEY_LEFTCTRL, uinput.KEY_C],
		"Next": uinput.KEY_TAB,
		"Send": uinput.KEY_ENTER,
		
		# Fix inverted chars
		"A": uinput.KEY_Q,
		"Q": uinput.KEY_A,
		"Z": uinput.KEY_W,
		"W": uinput.KEY_Z,
		"M": uinput.KEY_SEMICOLON,
		
		# Fix specials chars
		",": uinput.KEY_M,
		".": [uinput.KEY_LEFTSHIFT, uinput.KEY_COMMA],
		"'": uinput.KEY_4,
		";": uinput.KEY_COMMA,
		"-": uinput.KEY_6,
		":": uinput.KEY_DOT,
		"?": [uinput.KEY_LEFTSHIFT, uinput.KEY_M],
		
		# Fix special chars combo
		"Caps L + -": uinput.KEY_EQUAL,
		"Caps L + :": uinput.KEY_KPASTERISK,
		"Caps L + ?": [uinput.KEY_LEFTSHIFT, uinput.KEY_DOT],
		
		# Fix numbers
		"1": [uinput.KEY_LEFTSHIFT, uinput.KEY_1],
		"3": [uinput.KEY_LEFTSHIFT, uinput.KEY_2],
		"2": [uinput.KEY_LEFTSHIFT, uinput.KEY_3],
		"4": [uinput.KEY_LEFTSHIFT, uinput.KEY_4],
		"5": [uinput.KEY_LEFTSHIFT, uinput.KEY_5],
		"6": [uinput.KEY_LEFTSHIFT, uinput.KEY_6],
		"7": [uinput.KEY_LEFTSHIFT, uinput.KEY_7],
		"8": [uinput.KEY_LEFTSHIFT, uinput.KEY_8],
		"9": [uinput.KEY_LEFTSHIFT, uinput.KEY_9],
		"0": [uinput.KEY_LEFTSHIFT, uinput.KEY_0],
		
		# Fix numbers special chars
		"Caps L + 1": uinput.KEY_SLASH,
		
	}.get(name, None)
	
# Main loop
try:

	kp = keypad()

	pressed = None
	last = None

	kp.addObserver("AzertyMinitelConverter")
	kp.addExtraKey([uinput.KEY_F4, uinput.KEY_TAB, uinput.KEY_DOT, uinput.KEY_EQUAL, uinput.KEY_SLASH, uinput.KEY_END, uinput.KEY_LEFTBRACE, uinput.KEY_RIGHTBRACE])
	kp.start()
	
	print "Keyboard polling is started..."

	while True:
		k = kp.getKey() # key coordinates
		
		# No key are pressed
		if k == None:
			# If a key was pressed before, release it
			if pressed is not None:
				kp.onKeyRelease(kp.KEYNAME[pressed[0]][pressed[1]], kp.KEYPAD[pressed[0]][pressed[1]])
				pressed = None
			last = None
			continue
		
		# The state hasn't changed
		if k == last:
			time.sleep(0.05)
			continue
		
		# The current key pressed has returned back, so a second key was release
		if k == pressed:
			# Allowed key combinaison
			if kp.KEYNAME[pressed[0]][pressed[1]] in kp.ALLOW_COMBINE:
				kp.onKeyComboRelease(kp.KEYNAME[pressed[0]][pressed[1]], kp.KEYPAD[pressed[0]][pressed[1]], kp.KEYNAME[last[0]][last[1]], kp.KEYPAD[last[0]][last[1]])
			# Just two keys separately
			else:
				kp.onKeyRelease(kp.KEYNAME[last[0]][last[1]], kp.KEYPAD[last[0]][last[1]])
			last = pressed
			continue
		
		# Key name
		n = kp.KEYNAME[k[0]][k[1]]
		# uinput key
		r = kp.KEYPAD[k[0]][k[1]]
		# A second key was pressed
		if pressed is not None:
			# Allowed key combinaison
			if kp.KEYNAME[pressed[0]][pressed[1]] in kp.ALLOW_COMBINE:
				kp.onKeyComboPress(kp.KEYNAME[pressed[0]][pressed[1]], kp.KEYPAD[pressed[0]][pressed[1]], n, r)
			# Just two keys separately
			else:
				kp.onKeyPress(n, r)
		# A first key was pressed
		else:
			kp.onKeyPress(n, r)
			pressed = k
			
		last = k
		
except BaseException as e:
	print(e)

GPIO.cleanup()
