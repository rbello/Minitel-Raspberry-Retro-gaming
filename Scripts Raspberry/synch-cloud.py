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

### START OF CONFIGURATION

scan_dir = "./RetroPie/roms/"
scan_ext = [".srm", ".state", ".dat", ".nv", ".hi", ".hs", ".cfg", ".eep", ".fs"]
ws_api_key = "base32secret3232"
ws_url = "https://static.evolya.fr/cloud-superswag/"
console_name = "Console Minitel"

### END OF CONFIGURATION

import os
import hashlib
import time
import pyotp
import requests
import urllib2
from urlparse import urlparse

# Try to load cache file
print "STEP 1 - Gather current save state from remote server"
cache = {}

# Generate OTP
totp = pyotp.TOTP(ws_api_key)
otp = str(totp.now())
print "  One-time password:", otp

# Ask for remote cache
print "  Connecting to", "{uri.scheme}://{uri.netloc}/".format(uri=urlparse(ws_url)), "..."
r = requests.post(ws_url, data={"action": "GetCache", "key": otp, "console": console_name})
if r.status_code != 200:
	print "Error: unable to get remote cache (" + r.status_code + ")"
	sys.exit(0)

# Fetch lines from result and parse data
content = [l.strip() for l in r.content.split("\n")]
updateTime = ""
for line in content:
	if updateTime == "":
		updateTime = line
		continue
	row = line.split(" ", 3)
	cache[row[0]] = [int(row[1]), row[2]]
print "  Cache was updated on: ", updateTime
print "  Found objects in cache: ", len(cache)
print "  Success!"

# Working vars
cacheWrite = ""
changed = False
count_files = 0
count_changed = 0
count_unchanged = 0

# Fetch files in scanned directory, search for configuration/save state files,
# and do the comparison with stored cache.
print ""
print "Step 2 - Fetch local files..."
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
		# Check if file has changed
		if (md5 not in cache) or (mtime > cache[md5][0]):
			# Print a log
			print " ", path, md5, time.ctime(mtime)
			# Send files:
			# http://stackoverflow.com/questions/68477/send-file-using-post-from-a-python-script
			count_changed += 1
		else:
			count_unchanged += 1
