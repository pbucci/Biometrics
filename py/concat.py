#!//anaconda/bin/python

################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
################################################################################

import sys
import time
import os
def writeout(path,out):
	with open(path) as file:
		f = file.readlines()
	for line in f[1:]:
		out.write(line.strip() + '\n')

if len(sys.argv) < 2:
		print('Usage:', str(sys.argv))
		print('\t','python concat.py <csv1...n>')
		print('Assumes CSVs of the same shape + headers, vertical concatenation.\n', str(sys.argv))
else:
	print('Concatenating...')
	sys.stdout.flush()
	# timestamp for a unique filename
	timestamp = int(time.time())
	# make a new unique directory for CSVs to live in
	directory = "concatenated_csv" + "_" + str(timestamp)
	if not os.path.exists(directory):
		os.makedirs(directory)	

	with open(sys.argv[1]) as file:
		csv = file.readlines()

	concat = open(directory + '/' + 'concat' + '_' + str(timestamp) + '.' + 'csv','w+')
	concat.write(csv[0].strip() + '\n') # header

	for path in sys.argv[1:]:
		writeout(path,concat)

	concat.close()