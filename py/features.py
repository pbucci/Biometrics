#!//anaconda/bin/python

################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
################################################################################

import sys 
import os
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
from collections import OrderedDict

# ws    	is window size in ms
# fps   	is frames per second
# skp 		is gap in ms
# offset	is portion to cut off front and back in ms
# cols  	is list of column names
# data  	is the full dataset
def getRows(ws,fps,skp,offset,cols,data,features):
	fpms = float(fps) / 1000.0
	offset_in_frames = int( float(offset) * fpms )
	nrows = data.shape[0] -  (2 * offset_in_frames) # total number of rows - offset from front and back
	window_size_in_frames = int( ws * fpms )
	window_size_plus_skip_in_frames = int( (ws + skp) * fpms )
	ws_diff = window_size_plus_skip_in_frames - window_size_in_frames
	num_windows = math.floor(nrows / (window_size_plus_skip_in_frames))
	data_offset_removed = data[offset_in_frames:(nrows - offset_in_frames),:]
	
	# split array into chunks of window_size_in_frames rows deep
	# remainder frames are just dropped
	rows = []
	for i in range(0,num_windows): 
		
		m = i * window_size_plus_skip_in_frames
		n = ( (i+1) * window_size_plus_skip_in_frames ) - ws_diff

		line = []
		row_timestamp = math.floor(data[m,0] * 1000.0)
		
		for j in range(0,len(cols)):
			ret = featureVector(data_offset_removed[m:n,j],cols[j],features)
			line = line + ret
		rows.append(str(row_timestamp) + ',' + ','.join(line))
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
# features is an ordered dictionary of feature names -> functions
#		ex:
#			fd = {'mean' : np.mean, 'median':np.median}
def featureVector(data,columnname,features):
	arr = [v(data) for k,v in features.items()]
	# cut off float at 6 places for Weka
	filt = [format(x, ".6f") for x in arr]
	return [str(x) for x in filt] # turn this into string for writing out

# Do things like detrending...stub for now
def preprocess(data):
	return data # stub

def main():
	# Deal with arguments
	if len(sys.argv) < 6:
		print('Usage:', str(sys.argv))
		print('\t','python features.py <window_size_in_ms> <frames_per_second> <skip_length_ms> <offset_ms> <file1...n>')
	else:

		window_size_in_ms = int(sys.argv[1])
		frames_per_second = int(sys.argv[2])
		skip_length_ms    = int(sys.argv[3])
		offset_ms         = int(sys.argv[4])

		print('Calculating features for a window size of ' + str(window_size_in_ms) + "ms")

		# timestamp for a unique filename
		timestamp = int(time.time())
		
		# make a new unique directory for CSVs to live in
		directory = "window_size_in_ms_" + str(window_size_in_ms) #  + "_" + str(timestamp)
		
		if not os.path.exists(directory):
		    os.makedirs(directory)

		for path in sys.argv[5:]:
			print('Calculating features for ' + path + '...')
			sys.stdout.flush()
			
			# load data
			raw_data = np.loadtxt(path,skiprows=1,delimiter=',', dtype='float')

			# preprocess data (things like detrending, etc)
			data = preprocess(raw_data)

			# retrieve columns of CSV from first row
			columns = getColumns(path)
			
			# get particpant, condition, and emotion labels
			pn_cn_el = getMeta(path)
			
			# specify features
			featureDict = {
				'mean':np.mean,
				'median':np.median,
				'variance':np.var,
				'max':np.max,
				'min':np.min,
			}

			# sort features so you never have to worry about order
			features = OrderedDict(sorted(featureDict.items(), key=lambda t:t[0]))

			# generate rows of CSV
			# each row is a stringified set of features
			rows = getRows(window_size_in_ms,frames_per_second,skip_length_ms,offset_ms,columns,data,features)

			# construct the new CSV header and write it out to file
			header = 'timestamp,'
			for column in columns:
				header = header + ','.join([column + '_' + k for k in features.keys()]) + ','
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
