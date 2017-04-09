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

# Require PyOTP - The Python One-Time Password Library
# https://github.com/pyotp/pyotp
# Install : pip install pyotp

# Require Requests API
# Install : pip install requests

# Don't forget to setup time zone using raspi-config tool

ws_api_key = "LSX2I5BLGSXA4T77"
ws_url = "https://static.evolya.fr/cloud-superswag/"
console_name = "Minitel"

scan_dir = "./RetroPie/roms/"
scan_ext = [".state", ".state1", ".state2", ".state3", ".state4", ".state5", ".state6", ".state7", ".state8", ".state9", ".state0", ".dat", ".nv", ".hi", ".hs", ".cfg", ".eep", ".fs", ".sfc", ".st0", ".sra", ".fs"]

############ END OF CONFIGURATION ############

import os, sys
import hashlib
import time
import pyotp
import requests
import urllib2
from urlparse import urlparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Init cache
cache = {}

# Generate OTP
totp = pyotp.TOTP(ws_api_key)

# Ask for remote cache
print "  Connecting to", "{uri.scheme}://{uri.netloc}/".format(uri=urlparse(ws_url)), "..."
try:
	r = requests.get(ws_url)
	if r.status_code != 200:
		print bcolors.FAIL + "Error: unable to get remote cache (" + r.status_code + ")" + bcolors.ENDC
		sys.exit(1)
except Exception as e:
	print bcolors.FAIL + "Error: unable to get remote cache (" + str(e) + ")" + bcolors.ENDC
	sys.exit(1)

# Fetch lines from result and parse data
content = [l.strip() for l in r.content.split("\n")]
updateTime = ""
for line in content:
	if updateTime == "":
		updateTime = line.split(" ", 2)
		print "  Cache was updated on: ", updateTime[0], "(" + updateTime[1] + ")"
		continue
	row = line.split(" ", 5)
	# Format: cache[string md5] = [int mtime, string plateforme, int filesize, string filename]
	cache[row[0]] = [int(row[1]), row[2], int(row[3]), row[4]]
print "  Found objects in cache: ", len(cache)
print "  Success!"

# Working vars
cacheWrite = ""
changed = False
count_files = 0
count_changed = 0
count_unchanged = 0

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

# Fetch files in scanned directory, search for configuration/save state files,
# and do the comparison with stored cache.
print ""
print "Fetch local files..."
for root, directories, filenames in os.walk(scan_dir):
	for file in filenames:
		# File name and file extension
		filename, file_extension = os.path.splitext(file)
		# Avoid ignored files
		if file_extension not in scan_ext:
			continue
		count_files += 1
		# File full path
		path = os.path.join(root, file)
		# File hash
		md5 = hashlib.md5(path).hexdigest()
		# File last modification time
		mtime = os.path.getmtime(path)
		# Plateforme name
		plateforme = os.path.basename(os.path.dirname(path))
		# Change conditions
		change = None
		if md5 not in cache: change = "Hash"
		#elif mtime > cache[md5][0]: change = "Time"
		elif os.path.getsize(path) != cache[md5][2]: change = "Size"
		# Check if file has changed
		if change is not None:
			# Print a log
			print "   Upload: ", plateforme + "/" + file, "(" + sizeof_fmt(os.path.getsize(path)) + ", " + change + " change)"
			# Generate one time password
			otp = str(totp.now())
			# Begin upload
			with open(path, 'rb') as fd:
				# Post request
				r = requests.post(ws_url, files={file: fd}, data={'key': otp, 'console': console_name, 'hash': md5, 'mtime': mtime, 'plateforme': plateforme})
				if r.status_code != 200 and r.status_code != 201:
					print bcolors.FAIL + "  [FAILURE]", str(r.status_code), r.content, "=>", md5 + bcolors.ENDC
				else:
					print "  [SUCCESS]", md5, time.ctime(mtime), str(r.status_code), r.content
			count_changed += 1
		else:
			count_unchanged += 1

print "FINISHED !"
print "Updated:", count_changed, "Total:", (count_changed + count_unchanged)