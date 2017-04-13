#    _________                          _________                        
#   /   _____/__ ________   ___________/   _____/_  _  _______     ____  
#   \_____  \|  |  \____ \_/ __ \_  __ \_____  \\ \/ \/ /\__  \   / ___\ 
#   /        \  |  /  |_> >  ___/|  | \/        \\     /  / __ \_/ /_/  >
#  /_______  /____/|   __/ \___  >__| /_______  / \/\_/  (____  /\___  / 
#          \/      |__|        \/             \/              \//_____/  
#
# This file is a part of the SuperSwag projet.
# Copyleft 2017 - evolya.fr

import os, sys
import requests
import tzlocal
import hashlib
import urllib
import time
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

def download(otp, console_name, plateforme, game, url, path, file):

	# Get request
	args = {
		'key': otp,
		'console': console_name,
		'plateforme': plateforme,
		'gameid': game
	}
	r = requests.get(url + "?" + urllib.urlencode(args), stream=True)

	# Invalid response code
	if r.status_code != 200 and r.status_code != 201:
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", str(r.status_code), r.content
		return -1

	# Invalid response format
	if "GameID" not in r.headers or "Plateforme" not in r.headers or "FileChecksum" not in r.headers or "FileSize" not in r.headers or "FileMtime" not in r.headers:
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "Invalid headers (missing response attributes)", str(r.status_code), r.content
		return -2

	# Invalid file length (zero)
	if int(r.headers["FileSize"]) == 0:
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "File is newer on remote server but is empty:", plateforme, "/", file, "(" + game + ")"
		return -3

	# Invalid file length (different from contents)
	if int(r.headers["FileSize"]) != len(r.content):
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "Remote file has a different length:", plateforme, "/", file, "(" + game + ")"
		print "            Length:", int(r.headers["FileSize"]), "!= File:", len(r.content)
		return -4

	# Invalid file contents
	if r.headers["FileChecksum"] != hashlib.md5(r.content).hexdigest():
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "Remote file has a different checksum:", plateforme, "/", file, "(" + game + ")"
		print "            Header Checksum:", r.headers["FileChecksum"], "!= File:", hashlib.md5(r.content).hexdigest()
		print "            Header Length:", int(r.headers["FileSize"]), "== File:", len(r.content)
		return -5

	# Read and copy
	with open("./synch-cloud.tmp", "wb") as handle:
		for data in r.iter_content():
			handle.write(data)
	
	# Invalid file length (different from contents)
	if int(r.headers["FileSize"]) != os.path.getsize("./synch-cloud.tmp"):
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "Downloaded file has a different length:", plateforme, "/", file, "(" + game + ")"
		print "            Length:", int(r.headers["FileSize"]), "!= File:", os.path.getsize("./synch-cloud.tmp")				
		os.remove("./synch-cloud.tmp")
		return -6

	# Invalid file contents
	with open("./synch-cloud.tmp", "rb") as handle:
		md5 = hashlib.md5(handle.read()).hexdigest();
	if r.headers["FileChecksum"] != md5:
		print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", "Downloaded file has a different checksum:", plateforme, "/", file, "(" + game + ")"
		print "            Header Checksum:", r.headers["FileChecksum"], "!= File:", md5
		print "            Header Length:", int(r.headers["FileSize"]), "== File:", os.path.getsize("./synch-cloud.tmp")
		os.remove("./synch-cloud.tmp")
		return -7
		
	# Log
	print "  [" + bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC + "]", str(r.status_code), "(" + sizeof_fmt(int(r.headers["FileSize"])) + ", updated " + time.ctime(int(r.headers["FileMtime"])) + ")"
	
	# Move
	#print "   Rename ./synch-cloud.tmp -->", path
	os.rename("./synch-cloud.tmp", path)
	
	# Touch
	mtime = int(r.headers["FileMtime"])
	with open(path, 'a'): os.utime(path, (mtime, mtime))
	#print "   Touch ", time.ctime(mtime)
	
	return 0

def upload(otp, url, console_name, md5, mtime, plateforme, game, path, file):
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
			r = requests.post(url, files={file: fd}, data=args)
			#r = requests.post(url, files=IterableToFileAdapter(upload_in_chunks(path, chunksize=10)), data=args)
			#r = requests.post(url, files={file: IterableToFileAdapter(upload_in_chunks(path, chunksize=10))}, data=args)
			# Check status code
			if r.status_code != 200 and r.status_code != 201:
				print "  [" + bcolors.FAIL + "FAILURE" + bcolors.ENDC + "]", str(r.status_code), r.content
				return -1
			else:
				print "  [" + bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC + "]", time.ctime(mtime), str(r.status_code), r.content
				return 0
	except KeyboardInterrupt:
		print " INTERRUPT "
		sys.exit(2)
	except:
		ex = sys.exc_info()[0]
		print bcolors.FAIL + "  [FAILURE]", repr(ex.message), bcolors.ENDC
		raise

def loadcache(url, clientId):
	# Ask for remote cache
	print "Connecting to", "{uri.scheme}://{uri.netloc}/".format(uri=urlparse(url)), "from", clientId, "..."
	try:
		r = requests.get(url)
		if r.status_code != 200:
			print bcolors.FAIL + "Error: unable to get remote cache (" + r.status_code + ")" + bcolors.ENDC
			sys.exit(1)
	except Exception as e:
		print bcolors.FAIL + "Error: unable to get remote cache (" + str(e) + ")" + bcolors.ENDC
		sys.exit(1)

	# Fetch lines from result and parse data
	cache = {}
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
	return cache