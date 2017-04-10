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
import urllib
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

# Create OTP generator
totp = pyotp.TOTP(ws_api_key)

print bcolors.FAIL+"  __  "+bcolors.WARNING+" _    "+bcolors.OKGREEN+" ___   "+bcolors.ENDC+"____  "+bcolors.OKBLUE+"___     "+bcolors.FAIL+"__   "+bcolors.WARNING+"_        "+bcolors.OKGREEN+"__    "+bcolors.ENDC+"__   "
print bcolors.FAIL+" ( (` "+bcolors.WARNING+"| | | "+bcolors.OKGREEN+"| |_) "+bcolors.ENDC+"| |_  "+bcolors.OKBLUE+"| |_)   "+bcolors.FAIL+"( (` "+bcolors.WARNING+"\ \    / "+bcolors.OKGREEN+"/ /\  "+bcolors.ENDC+"/ /`_ "
print bcolors.FAIL+" _)_) "+bcolors.WARNING+"\_\_/ "+bcolors.OKGREEN+"|_|   "+bcolors.ENDC+"|_|__ "+bcolors.OKBLUE+"|_| \   "+bcolors.FAIL+"_)_)  "+bcolors.WARNING+"\_\/\/ "+bcolors.OKGREEN+"/_/--\ "+bcolors.ENDC+"\_\_/ "
print bcolors.ENDC

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
		if int(updateTime[1]) == 0:
			print "  Cache was never updated"
		else:
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
print "  Saves in remote cache:", len(cache)
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

class upload_in_chunks(object):
    def __init__(self, filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                sys.stderr.write("\r   {percent:3.0f}%".format(percent=percent))
                yield data

    def __len__(self):
        return self.totalsize

class IterableToFileAdapter(object):
    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.length = len(iterable)

    def read(self, size=-1): # TBD: add buffer for `len(data) > size` case
        return next(self.iterator, b'')

    def __len__(self):
        return self.length

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
		elif mtime > cache[game]["mtime"]: change = "Newer"
		elif mtime < cache[game]["mtime"]: change = "Older"
		#elif md5 != cache[game]["fileHash"]: change = "Hash"
		#elif os.path.getsize(path) != cache[game]["fileSize"]: change = "Size"
		
		if change is not None and change != "New" and md5 == cache[game]["fileHash"]:
			print "  [" + bcolors.WARNING + "WARNING" + bcolors.ENDC + "]", "File was updated on remote server without checksum change:", plateforme, "/", file, "(" + game + ")"
			continue
		
		# Check if file has changed
		if change is not None:
			action = "Upload"
			if change == "Older": action = "Download"
			# Print a log
			print "   " + action + ": ", plateforme, "/", file, "(" + sizeof_fmt(os.path.getsize(path)) + ", " + game + ", " + change + " change)"
			# Generate one time password
			otp = str(totp.now())
			# Begin upload
			if action == "Upload":
				try:
					with open(path, 'rb') as fd:
						# Post request
						args = {
							'key': otp,
							'console': console_name,
							'hash': md5,
							'mtime': mtime,
							'plateforme': plateforme,
							'gameid': game,
							'gamename': file
						}
						r = requests.post(ws_url, files={file: fd}, data=args)
						#r = requests.post(ws_url, files=IterableToFileAdapter(upload_in_chunks(path, chunksize=10)), data=args)
						#r = requests.post(ws_url, files={file: IterableToFileAdapter(upload_in_chunks(path, chunksize=10))}, data=args)
						# Check status code
						if r.status_code != 200 and r.status_code != 201:
							print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", str(r.status_code), r.content
							count_failures += 1
						else:
							print "  [" + bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC + "]", time.ctime(mtime), str(r.status_code), r.content
							count_changed += 1
				except KeyboardInterrupt:
					print " INTERRUPT "
					sys.exit(2)
				except:
					ex = sys.exc_info()[0]
					print bcolors.FAIL + "  [FAILURE]", repr(ex.message), bcolors.ENDC
					raise

			# Begin download
			else:
				# Get request
				args = {
					'key': otp,
					'console': console_name,
					'plateforme': plateforme,
					'gameid': game
				}
				r = requests.get(ws_url + "?" + urllib.urlencode(args))

				# Invalid response code
				if r.status_code != 200 and r.status_code != 201:
					print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", str(r.status_code), r.content
					count_failures += 1
					continue
				# Invalid response format
				if "GameID" not in r.headers or "Plateforme" not in r.headers or "FileChecksum" not in r.headers or "FileSize" not in r.headers or "FileMtime" not in r.headers:
					print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "Invalid headers (missing response attributes)", str(r.status_code), r.content
					count_failures += 1
					continue

				print "  [" + bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC + "]", str(r.status_code), "(" + sizeof_fmt(int(r.headers["FileSize"])) + ", updated " + time.ctime(int(r.headers["FileMtime"])) + ")", r.content
				count_changed += 1
				#sys.exit(111) # TODO

		# No change
		else:
			count_unchanged += 1

print bcolors.OKGREEN + "  FINISHED !" + bcolors.ENDC
print "  Updated:", count_changed, "Saves:", (count_changed + count_unchanged), "Failures:", count_failures