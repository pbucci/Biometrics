#!//anaconda/bin/python

################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
################################################################################
# Should only need to be run once...

import sys
import time
import os

if len(sys.argv) < 2:
	print("not enough arguments")
	print("Useage:")
	print("\tpython clean.py <file1...n>")
else:
	print('Cleaning started...')
	sys.stdout.flush()
	timestamp = int(time.time())
	directory = "clean" # + "_" + str(timestamp)
	
	if not os.path.exists(directory):
	    os.makedirs(directory)

	for path in sys.argv[1:]:
		print("Cleaning " + path + '...')
		sys.stdout.flush()
		filename = path.split('/')[-1]
		ext = filename.split('.')[-1]
		fn = filename.split('.')[0]
		
		with open(path) as file:
			f = file.readlines()
			f[6], f[7] = f[7], f[6] #
			out = open(directory + "/" + fn + "_clean_" + "." + ext, "w+")
			
			for line in f:
				line = line.strip()
				while len(line.split(',')) < 79:
					line = line.strip() + ",0"
				out.write(line.strip().replace('NM','0').replace('-1.#IO','0').replace('Switch to Screen','') + '\n')
			out.close()
		file.close()