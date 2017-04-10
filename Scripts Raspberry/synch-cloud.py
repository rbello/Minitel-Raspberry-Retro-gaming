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

# Require TZLOCAL time API
# Install : pip install tzlocal

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
import tzlocal

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
print "Connecting to", "{uri.scheme}://{uri.netloc}/".format(uri=urlparse(ws_url)), "..."
try:
	r = requests.get(ws_url)
	if r.status_code != 200:
		print bcolors.FAIL + "Error: unable to get remote cache (" + r.status_code + ")" + bcolors.ENDC
		sys.exit(1)
except Exception as e:
	print bcolors.FAIL + "Error: unable to get remote cache (" + str(e) + ")" + bcolors.ENDC
	sys.exit(1)

# Fetch lines from result and parse data
timezone = str(tzlocal.get_localzone())
updateTime = ""
content = [l.strip() for l in r.content.split("\n")]
for line in content:
	if updateTime == "":
		# Format: currentTime modificationTime timeZone
		updateTime = line.split(" ", 3)
		if updateTime[2] != timezone:
			print bcolors.FAIL + "  Error: timezone is not the same on the server (" + updateTime[2] + ") and this computer (" + timezone + ")" + bcolors.ENDC
			sys.exit(2)
		print "  Cache was updated on: ", time.ctime(int(updateTime[1])), "(" + updateTime[2] + ")"
		continue
	row = line.split("\t", 7)
	# Format: cache[string gameHash] = [string fileHash, int mtime, string plateforme, int filesize, string origin, string filename]
	cache[row[0]] = {
		"fileHash": row[1],
		"mtime": int(row[2]),
		"plateforme": row[3],
		"fileSize": int(row[4]),
		"console": row[5],
		"fileName": row[6]
	}
print "  Found objects in cache:", len(cache)
print bcolors.OKGREEN + "  Success!" + bcolors.ENDC

# Working vars
cacheWrite = ""
changed = False
count_files = 0
count_changed = 0
count_unchanged = 0
count_failures = 0

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
		# File full path
		path = os.path.join(root, file)
		# Plateforme name
		plateforme = os.path.basename(os.path.dirname(path))
		
		# Avoid ignored files
		if file_extension not in scan_ext: continue
		if "!" in path or "?" in path or "*" in path:
			print bcolors.WARNING + "  [WARNING]", "Avoid illegal file name:", plateforme, "/", file + bcolors.ENDC
			continue

		# Game name hash
		game = hashlib.md5(str(file)).hexdigest()[:8]
		# Save file checksum (hash)
		md5 = hashlib.md5(path).hexdigest()
		# File last modification time
		mtime = int(os.path.getmtime(path))
		
		# Add file count
		count_files += 1
		
		# Change conditions
		change = None
		if game not in cache: change = "New"
		elif mtime > cache[game]["mtime"]: change = "TimePlus"
		elif mtime < cache[game]["mtime"]: change = "TimeMinus"
		elif os.path.getsize(path) != cache[game]["fileSize"]: change = "Size"
		
		# Check if file has changed
		if change is not None:
			action = "Upload"
			if change == "TimeMinus": action = "Download"
			# Print a log
			print "   " + action + ": ", plateforme, "/", file, "(" + sizeof_fmt(os.path.getsize(path)) + ", ", game + ", " + change + " change)"
			# Generate one time password
			otp = str(totp.now())
			# Begin upload
			if action == "Upload":
				try:
					with open(path, 'rb') as fd:
						# Post request
						r = requests.post(ws_url, files={file: fd}, data={'key': otp, 'console': console_name, 'hash': md5, 'mtime': mtime, 'plateforme': plateforme, 'gameid': game, 'gamename': file})
						# Check status code
						if r.status_code != 200 and r.status_code != 201:
							print bcolors.FAIL + "  [FAILURE]", str(r.status_code), r.content + bcolors.ENDC
							count_failures += 1
						else:
							print "  [" + bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC + "]", time.ctime(mtime), str(r.status_code), r.content
							count_changed += 1
				except KeyboardInterrupt:
					print " INTERRUPT "
					sys.exit(2)
				except:
					print bcolors.FAIL + "  [FAILURE]", str(sys.exc_info()[0]) + bcolors.ENDC

			# Begin download
			else:
				pass

		# Times delta
		#elif int(mtime) != int(cache[md5][0]):
		#	print "   Fix time: ", plateforme + "/" + file, "(" + time.ctime(mtime) + " -> " + time.ctime(cache[md5][0]) + ", delta: " + str(mtime - cache[md5][0]) + "s)"

		# No change
		else:
			count_unchanged += 1

print bcolors.OKGREEN + "FINISHED !" + bcolors.ENDC
print "Updated:", count_changed, "Saves:", (count_changed + count_unchanged), "Failures:", count_failures