#!//anaconda/bin/python

################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
################################################################################

import sys
import os
import time
import math
import argparse

# skip the first 7 rows
skipheader = 7
if len(sys.argv) < 3:
	print('Usage:', str(sys.argv))
	print('\t','python reduce.py <hzr> <file1...n>')
else:
	timestamp = int(time.time())
	framerate = 2048
	hz = int(sys.argv[1])
	print('Reducing data to ' + str(hz) + ' hz')
	reduction_factor = math.floor(framerate / hz)
	directory = "reduce_by_" + str(hz) # + "_" + str(timestamp)
	if not os.path.exists(directory):
	    os.makedirs(directory)
	for path in sys.argv[2:]:
		print('Reducing ' + path + '...')
		with open(path) as file:
			f = file.readlines()[skipheader:]
			out = open(directory + '/' + path.split('/')[-1], 'w+')
			for i in range(0,len(f)):
				if (i % reduction_factor == 0):
					out.write(f[i])
			out.close()
		file.close()