################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
################################################################################
#!/usr/bin/python
import sys
import os
import time
import math

if len(sys.argv) < 3:
	print('Usage:', str(sys.argv))
	print('\t','python reduce.py <reduction_factor> <file1...n>')
else:
	# timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
	timestamp = int(time.time())
	framerate = 2048
	hz = int(sys.argv[1])
	reduction_factor = math.floor(framerate / hz)
	directory = "reduce_by_" + str(hz) + str(timestamp)
	if not os.path.exists(directory):
	    os.makedirs(directory)
	for fname in sys.argv[2:]:
		with open(fname) as file:
			f = file.readlines()
			out = open(directory + '/' + fname.split('/')[-1], 'w+')
			for i in range(0,len(f)):
				if (i % reduction_factor == 0):
					out.write(f[i])
			out.close()
		file.close()