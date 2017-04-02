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

import os
import hashlib
import time

dir = "./RetroPie/roms/"
ext = [".srm", ".state", ".dat", ".nv", ".hi", ".hs", ".cfg", ".eep", ".fs"]

out = open("./sync.dat", "w")
out.write("" + str(time.time()) + "\n")

for root, directories, filenames in os.walk(dir):
	for file in filenames:
		path = os.path.join(root, file)
		filename, file_extension = os.path.splitext(file)
		if file_extension in ext:
			md5 = hashlib.md5(path).hexdigest()
			mtime = os.path.getmtime(path)
			print path, md5, time.ctime(mtime)
			out.write(md5 + " " + str(mtime) + " " + path + "\n")

out.close()
