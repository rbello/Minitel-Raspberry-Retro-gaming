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
#@see https://github.com/tuomasjjrasanen/python-uinput/blob/master/src/ev.py

import uinput
import inspect
import sys

class uinputKeys():

	#KEY_RESERVED = (0x01, 0)
	#KEY_ESC = (0x01, 1)
	KEY_1 = (0x01, 2)
	KEY_2 = (0x01, 3)
	KEY_3 = (0x01, 4)
	KEY_4 = (0x01, 5)
	KEY_5 = (0x01, 6)
	KEY_6 = (0x01, 7)
	KEY_7 = (0x01, 8)
	KEY_8 = (0x01, 9)
	KEY_9 = (0x01, 10)
	KEY_0 = (0x01, 11)
	KEY_MINUS = (0x01, 12)
	KEY_EQUAL = (0x01, 13)
	KEY_BACKSPACE = (0x01, 14)
	KEY_TAB = (0x01, 15)
	KEY_Q = (0x01, 16)
	KEY_W = (0x01, 17)
	KEY_E = (0x01, 18)
	KEY_R = (0x01, 19)
	KEY_T = (0x01, 20)
	KEY_Y = (0x01, 21)
	KEY_U = (0x01, 22)
	KEY_I = (0x01, 23)
	KEY_O = (0x01, 24)
	KEY_P = (0x01, 25)
	KEY_LEFTBRACE = (0x01, 26)
	KEY_RIGHTBRACE = (0x01, 27)
	KEY_ENTER = (0x01, 28)
	KEY_LEFTCTRL = (0x01, 29)
	KEY_A = (0x01, 30)
	KEY_S = (0x01, 31)
	KEY_D = (0x01, 32)
	KEY_F = (0x01, 33)
	KEY_G = (0x01, 34)
	KEY_H = (0x01, 35)
	KEY_J = (0x01, 36)
	KEY_K = (0x01, 37)
	KEY_L = (0x01, 38)
	KEY_SEMICOLON = (0x01, 39)
	KEY_APOSTROPHE = (0x01, 40)
	KEY_GRAVE = (0x01, 41)
	KEY_LEFTSHIFT = (0x01, 42)
	KEY_BACKSLASH = (0x01, 43)
	KEY_Z = (0x01, 44)
	KEY_X = (0x01, 45)
	KEY_C = (0x01, 46)
	KEY_V = (0x01, 47)
	KEY_B = (0x01, 48)
	KEY_N = (0x01, 49)
	KEY_M = (0x01, 50)
	KEY_COMMA = (0x01, 51)
	KEY_DOT = (0x01, 52)
	KEY_SLASH = (0x01, 53)
	KEY_RIGHTSHIFT = (0x01, 54)
	KEY_KPASTERISK = (0x01, 55)
	KEY_LEFTALT = (0x01, 56)
	KEY_SPACE = (0x01, 57)
	KEY_CAPSLOCK = (0x01, 58)
	KEY_F1 = (0x01, 59)
	KEY_F2 = (0x01, 60)
	KEY_F3 = (0x01, 61)
	KEY_F4 = (0x01, 62)
	KEY_F5 = (0x01, 63)
	KEY_F6 = (0x01, 64)
	KEY_F7 = (0x01, 65)
	KEY_F8 = (0x01, 66)
	KEY_F9 = (0x01, 67)
	KEY_F10 = (0x01, 68)
	#KEY_NUMLOCK = (0x01, 69)
	#KEY_SCROLLLOCK = (0x01, 70)
	KEY_KP7 = (0x01, 71)
	KEY_KP8 = (0x01, 72)
	KEY_KP9 = (0x01, 73)
	KEY_KPMINUS = (0x01, 74)
	KEY_KP4 = (0x01, 75)
	KEY_KP5 = (0x01, 76)
	KEY_KP6 = (0x01, 77)
	KEY_KPPLUS = (0x01, 78)
	KEY_KP1 = (0x01, 79)
	KEY_KP2 = (0x01, 80)
	KEY_KP3 = (0x01, 81)
	KEY_KP0 = (0x01, 82)
	KEY_KPDOT = (0x01, 83)
	KEY_ZENKAKUHANKAKU = (0x01, 85)
	KEY_102ND = (0x01, 86)
	KEY_F11 = (0x01, 87)
	KEY_F12 = (0x01, 88)
	KEY_RO = (0x01, 89)
	KEY_KATAKANA = (0x01, 90)
	KEY_HIRAGANA = (0x01, 91)
	KEY_HENKAN = (0x01, 92)
	KEY_KATAKANAHIRAGANA = (0x01, 93)
	KEY_MUHENKAN = (0x01, 94)
	KEY_KPJPCOMMA = (0x01, 95)
	KEY_KPENTER = (0x01, 96)
	KEY_RIGHTCTRL = (0x01, 97)
	KEY_KPSLASH = (0x01, 98)
	KEY_SYSRQ = (0x01, 99)
	KEY_RIGHTALT = (0x01, 100)
	KEY_LINEFEED = (0x01, 101)
	KEY_HOME = (0x01, 102)
	KEY_UP = (0x01, 103)
	KEY_PAGEUP = (0x01, 104)
	KEY_LEFT = (0x01, 105)
	KEY_RIGHT = (0x01, 106)
	KEY_END = (0x01, 107)
	KEY_DOWN = (0x01, 108)
	KEY_PAGEDOWN = (0x01, 109)
	KEY_INSERT = (0x01, 110)
	KEY_DELETE = (0x01, 111)
	KEY_MACRO = (0x01, 112)
	KEY_MUTE = (0x01, 113)
	KEY_VOLUMEDOWN = (0x01, 114)
	KEY_VOLUMEUP = (0x01, 115)
	KEY_POWER = (0x01, 116)
	KEY_KPEQUAL = (0x01, 117)
	KEY_KPPLUSMINUS = (0x01, 118)
	KEY_PAUSE = (0x01, 119)
	KEY_SCALE = (0x01, 120)
	KEY_KPCOMMA = (0x01, 121)
	KEY_HANGEUL = (0x01, 122)
	KEY_HANGUEL = (0x01, 122)
	KEY_HANJA = (0x01, 123)
	KEY_YEN = (0x01, 124)
	KEY_LEFTMETA = (0x01, 125)
	KEY_RIGHTMETA = (0x01, 126)
	KEY_COMPOSE = (0x01, 127)
	KEY_STOP = (0x01, 128)
	KEY_AGAIN = (0x01, 129)
	KEY_PROPS = (0x01, 130)
	KEY_UNDO = (0x01, 131)
	KEY_FRONT = (0x01, 132)
	KEY_COPY = (0x01, 133)
	KEY_OPEN = (0x01, 134)
	KEY_PASTE = (0x01, 135)
	KEY_FIND = (0x01, 136)
	KEY_CUT = (0x01, 137)
	KEY_HELP = (0x01, 138)
	KEY_MENU = (0x01, 139)
	KEY_CALC = (0x01, 140)
	KEY_SETUP = (0x01, 141)
	KEY_SLEEP = (0x01, 142)
	KEY_WAKEUP = (0x01, 143)
	KEY_FILE = (0x01, 144)
	KEY_SENDFILE = (0x01, 145)
	KEY_DELETEFILE = (0x01, 146)
	KEY_XFER = (0x01, 147)
	KEY_PROG1 = (0x01, 148)
	KEY_PROG2 = (0x01, 149)
	KEY_WWW = (0x01, 150)
	KEY_MSDOS = (0x01, 151)
	KEY_COFFEE = (0x01, 152)
	KEY_SCREENLOCK = (0x01, 152)
	KEY_ROTATE_DISPLAY = (0x01, 153)
	KEY_DIRECTION = (0x01, 153)
	KEY_CYCLEWINDOWS = (0x01, 154)
	KEY_MAIL = (0x01, 155)
	KEY_BOOKMARKS = (0x01, 156)
	KEY_COMPUTER = (0x01, 157)
	KEY_BACK = (0x01, 158)
	KEY_FORWARD = (0x01, 159)
	KEY_CLOSECD = (0x01, 160)
	KEY_EJECTCD = (0x01, 161)
	KEY_EJECTCLOSECD = (0x01, 162)
	KEY_NEXTSONG = (0x01, 163)
	KEY_PLAYPAUSE = (0x01, 164)
	KEY_PREVIOUSSONG = (0x01, 165)
	KEY_STOPCD = (0x01, 166)
	KEY_RECORD = (0x01, 167)
	KEY_REWIND = (0x01, 168)
	KEY_PHONE = (0x01, 169)
	KEY_ISO = (0x01, 170)
	KEY_CONFIG = (0x01, 171)
	KEY_HOMEPAGE = (0x01, 172)
	KEY_REFRESH = (0x01, 173)
	KEY_EXIT = (0x01, 174)
	KEY_MOVE = (0x01, 175)
	KEY_EDIT = (0x01, 176)
	KEY_SCROLLUP = (0x01, 177)
	KEY_SCROLLDOWN = (0x01, 178)
	KEY_KPLEFTPAREN = (0x01, 179)
	KEY_KPRIGHTPAREN = (0x01, 180)
	KEY_NEW = (0x01, 181)
	KEY_REDO = (0x01, 182)
	KEY_F13 = (0x01, 183)
	KEY_F14 = (0x01, 184)
	KEY_F15 = (0x01, 185)
	KEY_F16 = (0x01, 186)
	KEY_F17 = (0x01, 187)
	KEY_F18 = (0x01, 188)
	KEY_F19 = (0x01, 189)
	KEY_F20 = (0x01, 190)
	KEY_F21 = (0x01, 191)
	KEY_F22 = (0x01, 192)
	KEY_F23 = (0x01, 193)
	KEY_F24 = (0x01, 194)
	KEY_PLAYCD = (0x01, 200)
	KEY_PAUSECD = (0x01, 201)
	KEY_PROG3 = (0x01, 202)
	KEY_PROG4 = (0x01, 203)
	KEY_DASHBOARD = (0x01, 204)
	KEY_SUSPEND = (0x01, 205)
	KEY_CLOSE = (0x01, 206)
	KEY_PLAY = (0x01, 207)
	KEY_FASTFORWARD = (0x01, 208)
	KEY_BASSBOOST = (0x01, 209)
	KEY_PRINT = (0x01, 210)
	KEY_HP = (0x01, 211)
	KEY_CAMERA = (0x01, 212)
	KEY_SOUND = (0x01, 213)
	KEY_QUESTION = (0x01, 214)
	KEY_EMAIL = (0x01, 215)
	KEY_CHAT = (0x01, 216)
	KEY_SEARCH = (0x01, 217)
	KEY_CONNECT = (0x01, 218)
	KEY_FINANCE = (0x01, 219)
	KEY_SPORT = (0x01, 220)
	KEY_SHOP = (0x01, 221)
	KEY_ALTERASE = (0x01, 222)
	KEY_CANCEL = (0x01, 223)
	KEY_BRIGHTNESSDOWN = (0x01, 224)
	KEY_BRIGHTNESSUP = (0x01, 225)
	KEY_MEDIA = (0x01, 226)
	KEY_SWITCHVIDEOMODE = (0x01, 227)
	KEY_KBDILLUMTOGGLE = (0x01, 228)
	KEY_KBDILLUMDOWN = (0x01, 229)
	KEY_KBDILLUMUP = (0x01, 230)
	KEY_SEND = (0x01, 231)
	KEY_REPLY = (0x01, 232)
	KEY_FORWARDMAIL = (0x01, 233)
	KEY_SAVE = (0x01, 234)
	KEY_DOCUMENTS = (0x01, 235)
	KEY_BATTERY = (0x01, 236)
	KEY_BLUETOOTH = (0x01, 237)
	KEY_WLAN = (0x01, 238)
	KEY_UWB = (0x01, 239)
	KEY_UNKNOWN = (0x01, 240)
	KEY_VIDEO_NEXT = (0x01, 241)
	KEY_VIDEO_PREV = (0x01, 242)
	KEY_BRIGHTNESS_CYCLE = (0x01, 243)
	KEY_BRIGHTNESS_AUTO = (0x01, 244)
	KEY_BRIGHTNESS_ZERO = (0x01, 244)
	KEY_DISPLAY_OFF = (0x01, 245)
	KEY_WWAN = (0x01, 246)
	KEY_WIMAX = (0x01, 246)
	KEY_RFKILL = (0x01, 247)
	KEY_MICMUTE = (0x01, 248)
	KEY_OK = (0x01, 0x160)
	KEY_SELECT = (0x01, 0x161)
	KEY_GOTO = (0x01, 0x162)
	KEY_CLEAR = (0x01, 0x163)
	KEY_POWER2 = (0x01, 0x164)
	KEY_OPTION = (0x01, 0x165)
	KEY_INFO = (0x01, 0x166)
	KEY_TIME = (0x01, 0x167)
	KEY_VENDOR = (0x01, 0x168)
	KEY_ARCHIVE = (0x01, 0x169)
	KEY_PROGRAM = (0x01, 0x16a)
	KEY_CHANNEL = (0x01, 0x16b)
	KEY_FAVORITES = (0x01, 0x16c)
	KEY_EPG = (0x01, 0x16d)
	KEY_PVR = (0x01, 0x16e)
	KEY_MHP = (0x01, 0x16f)
	KEY_LANGUAGE = (0x01, 0x170)
	KEY_TITLE = (0x01, 0x171)
	KEY_SUBTITLE = (0x01, 0x172)
	KEY_ANGLE = (0x01, 0x173)
	KEY_ZOOM = (0x01, 0x174)
	KEY_MODE = (0x01, 0x175)
	KEY_KEYBOARD = (0x01, 0x176)
	KEY_SCREEN = (0x01, 0x177)
	KEY_PC = (0x01, 0x178)
	KEY_TV = (0x01, 0x179)
	KEY_TV2 = (0x01, 0x17a)
	KEY_VCR = (0x01, 0x17b)
	KEY_VCR2 = (0x01, 0x17c)
	KEY_SAT = (0x01, 0x17d)
	KEY_SAT2 = (0x01, 0x17e)
	KEY_CD = (0x01, 0x17f)
	KEY_TAPE = (0x01, 0x180)
	KEY_RADIO = (0x01, 0x181)
	KEY_TUNER = (0x01, 0x182)
	KEY_PLAYER = (0x01, 0x183)
	KEY_TEXT = (0x01, 0x184)
	KEY_DVD = (0x01, 0x185)
	KEY_AUX = (0x01, 0x186)
	KEY_MP3 = (0x01, 0x187)
	KEY_AUDIO = (0x01, 0x188)
	KEY_VIDEO = (0x01, 0x189)
	KEY_DIRECTORY = (0x01, 0x18a)
	KEY_LIST = (0x01, 0x18b)
	KEY_MEMO = (0x01, 0x18c)
	KEY_CALENDAR = (0x01, 0x18d)
	KEY_RED = (0x01, 0x18e)
	KEY_GREEN = (0x01, 0x18f)
	KEY_YELLOW = (0x01, 0x190)
	KEY_BLUE = (0x01, 0x191)
	KEY_CHANNELUP = (0x01, 0x192)
	KEY_CHANNELDOWN = (0x01, 0x193)
	KEY_FIRST = (0x01, 0x194)
	KEY_LAST = (0x01, 0x195)
	KEY_AB = (0x01, 0x196)
	KEY_NEXT = (0x01, 0x197)
	KEY_RESTART = (0x01, 0x198)
	KEY_SLOW = (0x01, 0x199)
	KEY_SHUFFLE = (0x01, 0x19a)
	KEY_BREAK = (0x01, 0x19b)
	KEY_PREVIOUS = (0x01, 0x19c)
	KEY_DIGITS = (0x01, 0x19d)
	KEY_TEEN = (0x01, 0x19e)
	KEY_TWEN = (0x01, 0x19f)
	KEY_VIDEOPHONE = (0x01, 0x1a0)
	KEY_GAMES = (0x01, 0x1a1)
	KEY_ZOOMIN = (0x01, 0x1a2)
	KEY_ZOOMOUT = (0x01, 0x1a3)
	KEY_ZOOMRESET = (0x01, 0x1a4)
	KEY_WORDPROCESSOR = (0x01, 0x1a5)
	KEY_EDITOR = (0x01, 0x1a6)
	KEY_SPREADSHEET = (0x01, 0x1a7)
	KEY_GRAPHICSEDITOR = (0x01, 0x1a8)
	KEY_PRESENTATION = (0x01, 0x1a9)
	KEY_DATABASE = (0x01, 0x1aa)
	KEY_NEWS = (0x01, 0x1ab)
	KEY_VOICEMAIL = (0x01, 0x1ac)
	KEY_ADDRESSBOOK = (0x01, 0x1ad)
	KEY_MESSENGER = (0x01, 0x1ae)
	KEY_DISPLAYTOGGLE = (0x01, 0x1af)
	KEY_BRIGHTNESS_TOGGLE = (0x01, 0x1af)
	KEY_SPELLCHECK = (0x01, 0x1b0)
	KEY_LOGOFF = (0x01, 0x1b1)
	KEY_DOLLAR = (0x01, 0x1b2)
	KEY_EURO = (0x01, 0x1b3)
	KEY_FRAMEBACK = (0x01, 0x1b4)
	KEY_FRAMEFORWARD = (0x01, 0x1b5)
	KEY_CONTEXT_MENU = (0x01, 0x1b6)
	KEY_MEDIA_REPEAT = (0x01, 0x1b7)
	KEY_10CHANNELSUP = (0x01, 0x1b8)
	KEY_10CHANNELSDOWN = (0x01, 0x1b9)
	KEY_IMAGES = (0x01, 0x1ba)
	KEY_DEL_EOL = (0x01, 0x1c0)
	KEY_DEL_EOS = (0x01, 0x1c1)
	KEY_INS_LINE = (0x01, 0x1c2)
	KEY_DEL_LINE = (0x01, 0x1c3)
	KEY_FN = (0x01, 0x1d0)
	KEY_FN_ESC = (0x01, 0x1d1)
	KEY_FN_F1 = (0x01, 0x1d2)
	KEY_FN_F2 = (0x01, 0x1d3)
	KEY_FN_F3 = (0x01, 0x1d4)
	KEY_FN_F4 = (0x01, 0x1d5)
	KEY_FN_F5 = (0x01, 0x1d6)
	KEY_FN_F6 = (0x01, 0x1d7)
	KEY_FN_F7 = (0x01, 0x1d8)
	KEY_FN_F8 = (0x01, 0x1d9)
	KEY_FN_F9 = (0x01, 0x1da)
	KEY_FN_F10 = (0x01, 0x1db)
	KEY_FN_F11 = (0x01, 0x1dc)
	KEY_FN_F12 = (0x01, 0x1dd)
	KEY_FN_1 = (0x01, 0x1de)
	KEY_FN_2 = (0x01, 0x1df)
	KEY_FN_D = (0x01, 0x1e0)
	KEY_FN_E = (0x01, 0x1e1)
	KEY_FN_F = (0x01, 0x1e2)
	KEY_FN_S = (0x01, 0x1e3)
	KEY_FN_B = (0x01, 0x1e4)
	KEY_BRL_DOT1 = (0x01, 0x1f1)
	KEY_BRL_DOT2 = (0x01, 0x1f2)
	KEY_BRL_DOT3 = (0x01, 0x1f3)
	KEY_BRL_DOT4 = (0x01, 0x1f4)
	KEY_BRL_DOT5 = (0x01, 0x1f5)
	KEY_BRL_DOT6 = (0x01, 0x1f6)
	KEY_BRL_DOT7 = (0x01, 0x1f7)
	KEY_BRL_DOT8 = (0x01, 0x1f8)
	KEY_BRL_DOT9 = (0x01, 0x1f9)
	KEY_BRL_DOT10 = (0x01, 0x1fa)
	KEY_NUMERIC_0 = (0x01, 0x200)
	KEY_NUMERIC_1 = (0x01, 0x201)
	KEY_NUMERIC_2 = (0x01, 0x202)
	KEY_NUMERIC_3 = (0x01, 0x203)
	KEY_NUMERIC_4 = (0x01, 0x204)
	KEY_NUMERIC_5 = (0x01, 0x205)
	KEY_NUMERIC_6 = (0x01, 0x206)
	KEY_NUMERIC_7 = (0x01, 0x207)
	KEY_NUMERIC_8 = (0x01, 0x208)
	KEY_NUMERIC_9 = (0x01, 0x209)
	KEY_NUMERIC_STAR = (0x01, 0x20a)
	KEY_NUMERIC_POUND = (0x01, 0x20b)
	KEY_NUMERIC_A = (0x01, 0x20c)
	KEY_NUMERIC_B = (0x01, 0x20d)
	KEY_NUMERIC_C = (0x01, 0x20e)
	KEY_NUMERIC_D = (0x01, 0x20f)
	KEY_CAMERA_FOCUS = (0x01, 0x210)
	KEY_WPS_BUTTON = (0x01, 0x211)
	KEY_TOUCHPAD_TOGGLE = (0x01, 0x212)
	KEY_TOUCHPAD_ON = (0x01, 0x213)
	KEY_TOUCHPAD_OFF = (0x01, 0x214)
	KEY_CAMERA_ZOOMIN = (0x01, 0x215)
	KEY_CAMERA_ZOOMOUT = (0x01, 0x216)
	KEY_CAMERA_UP = (0x01, 0x217)
	KEY_CAMERA_DOWN = (0x01, 0x218)
	KEY_CAMERA_LEFT = (0x01, 0x219)
	KEY_CAMERA_RIGHT = (0x01, 0x21a)
	KEY_ATTENDANT_ON = (0x01, 0x21b)
	KEY_ATTENDANT_OFF = (0x01, 0x21c)
	KEY_ATTENDANT_TOGGLE = (0x01, 0x21d)
	KEY_LIGHTS_TOGGLE = (0x01, 0x21e)
	KEY_ALS_TOGGLE = (0x01, 0x230)
	KEY_BUTTONCONFIG = (0x01, 0x240)
	KEY_TASKMANAGER = (0x01, 0x241)
	KEY_JOURNAL = (0x01, 0x242)
	KEY_CONTROLPANEL = (0x01, 0x243)
	KEY_APPSELECT = (0x01, 0x244)
	KEY_SCREENSAVER = (0x01, 0x245)
	KEY_VOICECOMMAND = (0x01, 0x246)
	KEY_BRIGHTNESS_MIN = (0x01, 0x250)
	KEY_BRIGHTNESS_MAX = (0x01, 0x251)
	KEY_KBDINPUTASSIST_PREV = (0x01, 0x260)
	KEY_KBDINPUTASSIST_NEXT = (0x01, 0x261)
	KEY_KBDINPUTASSIST_PREVGROUP = (0x01, 0x262)
	KEY_KBDINPUTASSIST_NEXTGROUP = (0x01, 0x263)
	KEY_KBDINPUTASSIST_ACCEPT = (0x01, 0x264)
	KEY_KBDINPUTASSIST_CANCEL = (0x01, 0x265)
	KEY_MIN_INTERESTING = (0x01, 113)
	KEY_MAX = (0x01, 0x2ff)
	BTN_MISC = (0x01, 0x100)
	BTN_0 = (0x01, 0x100)
	BTN_1 = (0x01, 0x101)
	BTN_2 = (0x01, 0x102)
	BTN_3 = (0x01, 0x103)
	BTN_4 = (0x01, 0x104)
	BTN_5 = (0x01, 0x105)
	BTN_6 = (0x01, 0x106)
	BTN_7 = (0x01, 0x107)
	BTN_8 = (0x01, 0x108)
	BTN_9 = (0x01, 0x109)
	BTN_MOUSE = (0x01, 0x110)
	BTN_LEFT = (0x01, 0x110)
	BTN_RIGHT = (0x01, 0x111)
	BTN_MIDDLE = (0x01, 0x112)
	BTN_SIDE = (0x01, 0x113)
	BTN_EXTRA = (0x01, 0x114)
	BTN_FORWARD = (0x01, 0x115)
	BTN_BACK = (0x01, 0x116)
	BTN_TASK = (0x01, 0x117)
	BTN_JOYSTICK = (0x01, 0x120)
	BTN_TRIGGER = (0x01, 0x120)
	BTN_THUMB = (0x01, 0x121)
	BTN_THUMB2 = (0x01, 0x122)
	BTN_TOP = (0x01, 0x123)
	BTN_TOP2 = (0x01, 0x124)
	BTN_PINKIE = (0x01, 0x125)
	BTN_BASE = (0x01, 0x126)
	BTN_BASE2 = (0x01, 0x127)
	BTN_BASE3 = (0x01, 0x128)
	BTN_BASE4 = (0x01, 0x129)
	BTN_BASE5 = (0x01, 0x12a)
	BTN_BASE6 = (0x01, 0x12b)
	BTN_DEAD = (0x01, 0x12f)
	BTN_GAMEPAD = (0x01, 0x130)
	BTN_SOUTH = (0x01, 0x130)
	BTN_A = (0x01, 0x130)
	BTN_EAST = (0x01, 0x131)
	BTN_B = (0x01, 0x131)
	BTN_C = (0x01, 0x132)
	BTN_NORTH = (0x01, 0x133)
	BTN_X = (0x01, 0x133)
	BTN_WEST = (0x01, 0x134)
	BTN_Y = (0x01, 0x134)
	BTN_Z = (0x01, 0x135)
	BTN_TL = (0x01, 0x136)
	BTN_TR = (0x01, 0x137)
	BTN_TL2 = (0x01, 0x138)
	BTN_TR2 = (0x01, 0x139)
	BTN_SELECT = (0x01, 0x13a)
	BTN_START = (0x01, 0x13b)
	BTN_MODE = (0x01, 0x13c)
	BTN_THUMBL = (0x01, 0x13d)
	BTN_THUMBR = (0x01, 0x13e)
	BTN_DIGI = (0x01, 0x140)
	BTN_TOOL_PEN = (0x01, 0x140)
	BTN_TOOL_RUBBER = (0x01, 0x141)
	BTN_TOOL_BRUSH = (0x01, 0x142)
	BTN_TOOL_PENCIL = (0x01, 0x143)
	BTN_TOOL_AIRBRUSH = (0x01, 0x144)
	BTN_TOOL_FINGER = (0x01, 0x145)
	BTN_TOOL_MOUSE = (0x01, 0x146)
	BTN_TOOL_LENS = (0x01, 0x147)
	BTN_TOOL_QUINTTAP = (0x01, 0x148)
	BTN_TOUCH = (0x01, 0x14a)
	BTN_STYLUS = (0x01, 0x14b)
	BTN_STYLUS2 = (0x01, 0x14c)
	BTN_TOOL_DOUBLETAP = (0x01, 0x14d)
	BTN_TOOL_TRIPLETAP = (0x01, 0x14e)
	BTN_TOOL_QUADTAP = (0x01, 0x14f)
	BTN_WHEEL = (0x01, 0x150)
	BTN_GEAR_DOWN = (0x01, 0x150)
	BTN_GEAR_UP = (0x01, 0x151)
	BTN_DPAD_UP = (0x01, 0x220)
	BTN_DPAD_DOWN = (0x01, 0x221)
	BTN_DPAD_LEFT = (0x01, 0x222)
	BTN_DPAD_RIGHT = (0x01, 0x223)
	BTN_TRIGGER_HAPPY = (0x01, 0x2c0)
	BTN_TRIGGER_HAPPY1 = (0x01, 0x2c0)
	BTN_TRIGGER_HAPPY2 = (0x01, 0x2c1)
	BTN_TRIGGER_HAPPY3 = (0x01, 0x2c2)
	BTN_TRIGGER_HAPPY4 = (0x01, 0x2c3)
	BTN_TRIGGER_HAPPY5 = (0x01, 0x2c4)
	BTN_TRIGGER_HAPPY6 = (0x01, 0x2c5)
	BTN_TRIGGER_HAPPY7 = (0x01, 0x2c6)
	BTN_TRIGGER_HAPPY8 = (0x01, 0x2c7)
	BTN_TRIGGER_HAPPY9 = (0x01, 0x2c8)
	BTN_TRIGGER_HAPPY10 = (0x01, 0x2c9)
	BTN_TRIGGER_HAPPY11 = (0x01, 0x2ca)
	BTN_TRIGGER_HAPPY12 = (0x01, 0x2cb)
	BTN_TRIGGER_HAPPY13 = (0x01, 0x2cc)
	BTN_TRIGGER_HAPPY14 = (0x01, 0x2cd)
	BTN_TRIGGER_HAPPY15 = (0x01, 0x2ce)
	BTN_TRIGGER_HAPPY16 = (0x01, 0x2cf)
	BTN_TRIGGER_HAPPY17 = (0x01, 0x2d0)
	BTN_TRIGGER_HAPPY18 = (0x01, 0x2d1)
	BTN_TRIGGER_HAPPY19 = (0x01, 0x2d2)
	BTN_TRIGGER_HAPPY20 = (0x01, 0x2d3)
	BTN_TRIGGER_HAPPY21 = (0x01, 0x2d4)
	BTN_TRIGGER_HAPPY22 = (0x01, 0x2d5)
	BTN_TRIGGER_HAPPY23 = (0x01, 0x2d6)
	BTN_TRIGGER_HAPPY24 = (0x01, 0x2d7)
	BTN_TRIGGER_HAPPY25 = (0x01, 0x2d8)
	BTN_TRIGGER_HAPPY26 = (0x01, 0x2d9)
	BTN_TRIGGER_HAPPY27 = (0x01, 0x2da)
	BTN_TRIGGER_HAPPY28 = (0x01, 0x2db)
	BTN_TRIGGER_HAPPY29 = (0x01, 0x2dc)
	BTN_TRIGGER_HAPPY30 = (0x01, 0x2dd)
	BTN_TRIGGER_HAPPY31 = (0x01, 0x2de)
	BTN_TRIGGER_HAPPY32 = (0x01, 0x2df)
	BTN_TRIGGER_HAPPY33 = (0x01, 0x2e0)
	BTN_TRIGGER_HAPPY34 = (0x01, 0x2e1)
	BTN_TRIGGER_HAPPY35 = (0x01, 0x2e2)
	BTN_TRIGGER_HAPPY36 = (0x01, 0x2e3)
	BTN_TRIGGER_HAPPY37 = (0x01, 0x2e4)
	BTN_TRIGGER_HAPPY38 = (0x01, 0x2e5)
	BTN_TRIGGER_HAPPY39 = (0x01, 0x2e6)
	BTN_TRIGGER_HAPPY40 = (0x01, 0x2e7)
	REL_X = (0x02, 0x00)
	REL_Y = (0x02, 0x01)
	REL_Z = (0x02, 0x02)
	REL_RX = (0x02, 0x03)
	REL_RY = (0x02, 0x04)
	REL_RZ = (0x02, 0x05)
	REL_HWHEEL = (0x02, 0x06)
	REL_DIAL = (0x02, 0x07)
	REL_WHEEL = (0x02, 0x08)
	REL_MISC = (0x02, 0x09)
	REL_MAX = (0x02, 0x0f)
	ABS_X = (0x03, 0x00)
	ABS_Y = (0x03, 0x01)
	ABS_Z = (0x03, 0x02)
	ABS_RX = (0x03, 0x03)
	ABS_RY = (0x03, 0x04)
	ABS_RZ = (0x03, 0x05)
	ABS_THROTTLE = (0x03, 0x06)
	ABS_RUDDER = (0x03, 0x07)
	ABS_WHEEL = (0x03, 0x08)
	ABS_GAS = (0x03, 0x09)
	ABS_BRAKE = (0x03, 0x0a)
	ABS_HAT0X = (0x03, 0x10)
	ABS_HAT0Y = (0x03, 0x11)
	ABS_HAT1X = (0x03, 0x12)
	ABS_HAT1Y = (0x03, 0x13)
	ABS_HAT2X = (0x03, 0x14)
	ABS_HAT2Y = (0x03, 0x15)
	ABS_HAT3X = (0x03, 0x16)
	ABS_HAT3Y = (0x03, 0x17)
	ABS_PRESSURE = (0x03, 0x18)
	ABS_DISTANCE = (0x03, 0x19)
	ABS_TILT_X = (0x03, 0x1a)
	ABS_TILT_Y = (0x03, 0x1b)
	ABS_TOOL_WIDTH = (0x03, 0x1c)
	ABS_VOLUME = (0x03, 0x20)
	ABS_MISC = (0x03, 0x28)
	ABS_MT_SLOT = (0x03, 0x2f)
	ABS_MT_TOUCH_MAJOR = (0x03, 0x30)
	ABS_MT_TOUCH_MINOR = (0x03, 0x31)
	ABS_MT_WIDTH_MAJOR = (0x03, 0x32)
	ABS_MT_WIDTH_MINOR = (0x03, 0x33)
	ABS_MT_ORIENTATION = (0x03, 0x34)
	ABS_MT_POSITION_X = (0x03, 0x35)
	ABS_MT_POSITION_Y = (0x03, 0x36)
	ABS_MT_TOOL_TYPE = (0x03, 0x37)
	ABS_MT_BLOB_ID = (0x03, 0x38)
	ABS_MT_TRACKING_ID = (0x03, 0x39)
	ABS_MT_PRESSURE = (0x03, 0x3a)
	ABS_MT_DISTANCE = (0x03, 0x3b)
	ABS_MT_TOOL_X = (0x03, 0x3c)
	ABS_MT_TOOL_Y = (0x03, 0x3d)
	ABS_MAX = (0x03, 0x3f)

keys = []
attributes = inspect.getmembers(uinputKeys, lambda a:not(inspect.isroutine(a)))
list = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
for key in list:
	keys.append(key[1])

device = uinput.Device(keys)

col = 0
maxCol = 10
for key in list:
	col = col + 1
	if col > maxCol:
		col = 0
		input("Press Enter to continue...")
	
	sys.stdout.write(key[0] + "=" + str(key[1]) + "=")
	sys.stdout.flush()
	#try:
	#	device.emit_click(key[1])
	#except:
	#	pass
	sys.stdout.write("\n")
	sys.stdout.flush()