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
import re
import numpy as np

# ws    is window size in seconds
# fps   is frames per second
# cols  is list of column names
# data  is the full dataset
def getRows(ws,fps,cols,data):
	nrows = data.shape[0] # number of rows
	window_size_in_frames = ws * (float(fps) / 1000.0)
	num_windows = math.floor(nrows / window_size_in_frames)
	
	# split array into chunks of window_size_in_frames rows deep
	# remainder frames are just dropped
	rows = []
	for i in range(0,num_windows): 
		m = i * window_size_in_frames
		n = (i+1) * window_size_in_frames

		line = []
		for j in range(0,len(cols)):
			ret = featureVector(data[m:n,j],cols[j])
			line = line + ret
		rows.append(','.join(line))
	return rows

# Reads the first line of the CSV for column headers
def getColumns(path):
	with open(path) as cn:
		# str.replace(/foo/g, "bar")
		ret = re.sub(r'[:%\s\&\(\)/]','_',cn.readlines()[0].strip())
	return ret.split(',')

# gets the metadata from a file esp. participant num, condition, emotion
def getMeta(path):
	filename = path.split('/')[-1]
	pn_cn_el = filename.split('_')[0].split('-') # [ participant_number, condition_number, emotion label ]
	if len(pn_cn_el) < 3: # resting conditions don't have emotion labels
		pn_cn_el.append("None")
	return pn_cn_el


# all features 
# TODO make a dictionary for features + functions so this 
# can be automatically built
def featureVector(data,columnname):
	arr = [
		np.mean(data),    # mean
		np.median(data),  # median
		np.var(data)      # variance
	]

	return [str(x) for x in arr] # turn this into string for writing out

def main():
	# Deal with arguments
	if len(sys.argv) < 4:
		print('Usage:', str(sys.argv))
		print('\t','python features.py <window_size_in_ms> <frames_per_second> <file1...n>')
	else:

		window_size_in_ms = int(sys.argv[1])
		frames_per_second = int(sys.argv[2])

		print('Calculating features for a window size of ' + str(window_size_in_ms) + "ms")

		# timestamp for a unique filename
		timestamp = int(time.time())
		
		# make a new unique directory for CSVs to live in
		directory = "window_size_in_ms_" + str(window_size_in_ms)#  + "_" + str(timestamp)
		
		if not os.path.exists(directory):
		    os.makedirs(directory)

		for path in sys.argv[3:]:
			print('Calculating features for ' + path + '...')
			sys.stdout.flush()
			
			# load data
			data = np.loadtxt(path,skiprows=1,delimiter=',', dtype='float')

			# retrieve columns of CSV from first row
			columns = getColumns(path)
			
			# get particpant, condition, and emotion labels
			pn_cn_el = getMeta(path)
			
			# generate rows of CSV
			# each row is a stringified set of features
			rows = getRows(window_size_in_ms,frames_per_second,columns,data)

			# construct the new CSV header and write it out to file
			header = ''
			for column in columns:
				header = header + column + '_mean' + ',' + column + '_median' + ',' + column + '_variance' + ','
			header = header + "participant_number" + ',' + 'condition_number' + ',' + 'emotion_label'

			# make a new file to write to
			outfile = open(directory + '/' + '_'.join(pn_cn_el) + '_' + 'out' + '.' + 'csv', 'w+')

			outfile.write(header + '\n')

			# write all CSV rows to file
			for line in rows:
				line = line + ',' + ','.join(pn_cn_el) # make sure each line has 
				outfile.write(line + '\n')

if __name__ == '__main__':
	main()