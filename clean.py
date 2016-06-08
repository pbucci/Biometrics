#!/usr/bin/python

################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
################################################################################

import sys
skiplines = 8 # indexes at 1
print('Argument List:', str(sys.argv))
length = 0
count = 0

if len(sys.argv) < 2:
	print("not enough arguments")
else:
	for fname in sys.argv[1:]:
		with open(fname) as file:
			f = file.readlines()
			filename = fname.split('.')
			ext = filename[-1]
			name = '.'.join(filename[0:-1])
			out = open(name + "_clean" + "." + ext, 'w+')
			for i in range(skiplines,len(f)):
				count = count + 1
				line = f[i]
				if (len(line.split(',')) != length):
					length = len(line.split(','))
					print(line)
					print(count)
				out.write(line.strip().replace('NM','0').replace('-1.#IO','0').replace('Switch to Screen','') + '\n')
			out.close()
		file.close()