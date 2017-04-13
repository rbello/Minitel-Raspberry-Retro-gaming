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

# Before using this script install python modules : pip install pyotp requests tzlocal

# Don't forget to setup time zone using raspi-config tool

# Your saves states must be stores in /RetroPie/saves/
# Edit the file /opt/retropie/configs/all/retroarch.cfg
# And set :
#   savefile_directory = "/home/pi/RetroPie/saves/"
#   savestate_directory = "/home/pi/RetroPie/saves/"

scan_dir = "/home/pi/RetroPie/saves/"
scan_ext = [".state", ".state1", ".state2", ".state3", ".state4", ".state5", ".state6", ".state7", ".state8", ".state9", ".state0", ".dat", ".nv", ".hi", ".hs", ".cfg", ".eep", ".fs", ".sfc", ".st0", ".sra", ".fs"]
simulation = False

############ END OF CONFIGURATION ############

import os, sys
import hashlib
import pyotp
import synchlib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Extract command arguments
if len(sys.argv) < 4:
	print bcolors.FAIL + "Usage: synch-cloud.py <consoleName> <secretKey> <remoteUrl>" + bcolors.ENDC
	sys.exit(1)
console_name = sys.argv[1]
ws_api_key = sys.argv[2]
ws_url = sys.argv[3]

# Create OTP generator
totp = pyotp.TOTP(ws_api_key)

# Welcome message
print bcolors.FAIL+"  __  "+bcolors.WARNING+" _    "+bcolors.OKGREEN+" ___   "+bcolors.ENDC+"____  "+bcolors.OKBLUE+"___     "+bcolors.FAIL+"__   "+bcolors.WARNING+"_        "+bcolors.OKGREEN+"__    "+bcolors.ENDC+"__   "
print bcolors.FAIL+" ( (` "+bcolors.WARNING+"| | | "+bcolors.OKGREEN+"| |_) "+bcolors.ENDC+"| |_  "+bcolors.OKBLUE+"| |_)   "+bcolors.FAIL+"( (` "+bcolors.WARNING+"\ \    / "+bcolors.OKGREEN+"/ /\  "+bcolors.ENDC+"/ /`_ "
print bcolors.FAIL+" _)_) "+bcolors.WARNING+"\_\_/ "+bcolors.OKGREEN+"|_|   "+bcolors.ENDC+"|_|__ "+bcolors.OKBLUE+"|_| \   "+bcolors.FAIL+"_)_)  "+bcolors.WARNING+"\_\/\/ "+bcolors.OKGREEN+"/_/--\ "+bcolors.ENDC+"\_\_/ "
print bcolors.ENDC

# Init cache
cache = synchlib.loadcache(ws_url, console_name)

# Working vars
count_files = 0
count_changed = 0
count_unchanged = 0
count_failures = 0

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
			print "  [" + bcolors.WARNING + "WARNING" + bcolors.ENDC + "]", "Avoid illegal file name:", plateforme, "/", file
			count_unchanged += 1
			continue

		# Game name hash
		game = hashlib.md5(str(file)).hexdigest()[:8]
		# Save file checksum (hash)
		with open(path, "rb") as handle:
			md5 = hashlib.md5(handle.read()).hexdigest();
		# File last modification time
		mtime = int(os.path.getmtime(path))
		
		# Add file count
		count_files += 1
		
		# Change conditions
		change = None
		if game not in cache: change = "New"
		elif mtime > cache[game]["mtime"]: change = "Newer"
		elif mtime < cache[game]["mtime"]: change = "Older"
		#elif md5 != cache[game]["fileHash"]: change = "Hash"
		#elif os.path.getsize(path) != cache[game]["fileSize"]: change = "Size"
		
		if change is not None and change != "New" and md5 == cache[game]["fileHash"]:
			print "  [" + bcolors.WARNING + "WARNING" + bcolors.ENDC + "]", "Avoid: File is newer on remote server but without checksum change:", plateforme, "/", file, "(" + game + ")"
			if game in cache: del cache[game] # Remove from cache
			count_unchanged += 1
			continue
		
		if game in cache: del cache[game] # Remove from cache
		
		# Check if file has changed
		if change is not None:
			# Choose action
			action = "Upload"
			if change == "Older": action = "Download"
			# Print a log
			print "   " + action + ": ", plateforme, "/", file, "(" + synchlib.sizeof_fmt(os.path.getsize(path)) + ", " + game + ", " + change + " change)"
			# Simulation
			if simulation == True: continue
			# Generate one time password
			otp = str(totp.now())
			# Begin upload
			if action == "Upload":
				r = synchlib.upload(otp, ws_url, console_name, md5, mtime, plateforme, game, path, file)
				if r == 0: count_changed += 1
				else: count_failures += 1
			# Begin download
			if action == "Download":
				r = synchlib.download(otp, console_name, plateforme, game, ws_url, path, file)
				if r == 0: count_changed += 1
				else: count_failures += 1
		# No change
		else:
			if simulation == True:
				print "   Unchanged:", game, plateforme, "/", file
			count_unchanged += 1

if len(cache) > 0:
	print ""
	print "Fetch new remote files:", len(cache)
	for game in cache:
		plateforme = cache[game]["plateforme"]
		file = cache[game]["fileName"]
		print "  Download:", game, plateforme, "/", file
		# Simulation
		if simulation == True: continue
		otp = str(totp.now())
		path = scan_dir + plateforme + "/" + file
		r = synchlib.download(otp, console_name, plateforme, game, ws_url, path, file)
		if r == 0: count_changed += 1
		else: count_failures += 1

print ""
print bcolors.OKGREEN + "Finished !" + bcolors.ENDC
print "Updated:", count_changed, "Ignored:", count_unchanged, "Failures:", count_failures, "Total:", (count_changed + count_unchanged)