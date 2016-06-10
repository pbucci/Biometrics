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
import numpy as np

def featureVector(window):
	mean = np.mean(window)
	median = np.median(window)
	variance = np.var(window)
	return mean # stub

columns = ["Time","B: BVP","C: EMG","D: EMG","E: Skin Cond","F: Temp","G: Abd Resp","H: Thor Resp (optional)","B: BVP amplitude","B: BVP IBI","B: BVP HR from IBI","B: BVP HR (Smoothed)","B: BVP IBI peak freq.","B: BVP VLF % power","B: BVP LF % power","B: BVP HF % power","B: BVP VLF Total power","B: BVP LF Total power","B: BVP HF Total power","C: EMG + Smoothing","D: EMG + Smoothing","C&D: C:EMG - D:EMG","C&D: C:EMG + D:EMG","C&D: EMG C-D/C+D (balance fb)","E: SC as % of value","F: Temp as % of value","G: Resp Amplitude (Abd)","G: Resp period","G: Resp rate","B&G: HR max - HR min","H: Resp amplitude (thor)","G&H: Abd - Thor amplitude diff","B: BVP HR epoch mean","B: BVP IBI epoch std dev","B: BVP VLF % power ep mean","B: BVP LF % power ep mean","B: BVP HF % power ep mean","B: BVP VLF Total power ep mean","B: BVP LF Total power ep mean","B: BVP HF Total power ep mean","B: BVP LF/HF (ep means)","C: EMG epoch mean","D: EMG epoch mean","E: SC epoch mean","F: Temp epoch mean","G: Resp rate epoch mean","B: BVP amplitude mean (Rel)","B: BVP HR mean (beats/min)","B: BVP HR std. dev.","B: BVP peak freq. mean (Hz)","B: BVP IBI std. dev. (SDRR)","B: BVP VLF % power mean","B: BVP LF % power mean","B: BVP HF % power mean","B: BVP VLF total power mean","B: BVP LF Total power mean","B: BVP HF total power mean","B: BVP LF/HF (means)","C: EMG mean (uV)","D: EMG mean (uV)","E: Skin conductance mean (uS)","E: SC as % of value mean (%)","F: Temperature mean (Deg)","F: Temp as % of value mean (%)","G: Resp rate mean (br/min)","B&G: (HR max-min) mean (b/min)","G: Abd amplitude mean (rel)","H: Thor amplitude mean (rel)","G&H: Abd-tho ampl diff (means)","B: BVP IBI Peak amplitude","B: BVP IBI Pk ampl maximum","B: BVP IBI pk freq trigger","B: BVP IBI pk ampl trigger","H: Resp rate trigger","B: BVP IBI NN Intervals","B: BVP IBI pNN Intervals","B: BVP IBI pNN Intervals (%)","Event"]

def main():
	if len(sys.argv) < 3:
		print('Usage:', str(sys.argv))
		print('\t','python partition.py <file1...n>')
	else:
		# deal with filename stuff
		timestamp = int(time.time())
		# exmaple filename = the/path/to/folder/p11-r1_clean.csv
		path = sys.argv[1]
		filename = path.split('/')[-1]
		pn_cn_el = filename.split('_')[0].split('-') # [ participant_number, condition_number, emotion label ]
		if len(pn_cn_el) < 3: # resting conditions don't have emotion labels
			pn_cn_el.append("None")

		out = open('output' + "_" + str(timestamp) + ".csv",'w+')

		data = np.loadtxt(path, dtype=float, delimiter=',')
		
		print(data.dtype.names())
		
		dims = data.shape()
		# iterate through columns
		for i in range(0,dims[0]):
			column = data[:,i]
			# iterate through windows of size 2sec
			size_in_seconds = 2
			frames_per_second = 54
			window_size = size_in_seconds * frames_per_second
			for window in np.array_split(column,window_size):
				feature_vector = featureVector(window)


if __name__ == '__main__':
	main()