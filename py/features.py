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
from scipy import signal
from scipy.signal import butter, lfilter
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

# [timestamp,Time_max,Time_mean,Time_median,Time_min,Time_variance,B__BVP_max,B__BVP_mean,B__BVP_median,B__BVP_min,B__BVP_variance,C__EMG_max,C__EMG_mean,C__EMG_median,C__EMG_min,C__EMG_variance,D__EMG_max,D__EMG_mean,D__EMG_median,D__EMG_min,D__EMG_variance,E__Skin_Cond_max,E__Skin_Cond_mean,E__Skin_Cond_median,E__Skin_Cond_min,E__Skin_Cond_variance,F__Temp_max,F__Temp_mean,F__Temp_median,F__Temp_min,F__Temp_variance,G__Abd_Resp_max,G__Abd_Resp_mean,G__Abd_Resp_median,G__Abd_Resp_min,G__Abd_Resp_variance,H__Thor_Resp__optional__max,H__Thor_Resp__optional__mean,H__Thor_Resp__optional__median,H__Thor_Resp__optional__min,H__Thor_Resp__optional__variance,B__BVP_amplitude_max,B__BVP_amplitude_mean,B__BVP_amplitude_median,B__BVP_amplitude_min,B__BVP_amplitude_variance,B__BVP_IBI_max,B__BVP_IBI_mean,B__BVP_IBI_median,B__BVP_IBI_min,B__BVP_IBI_variance,B__BVP_HR_from_IBI_max,B__BVP_HR_from_IBI_mean,B__BVP_HR_from_IBI_median,B__BVP_HR_from_IBI_min,B__BVP_HR_from_IBI_variance,B__BVP_HR__Smoothed__max,B__BVP_HR__Smoothed__mean,B__BVP_HR__Smoothed__median,B__BVP_HR__Smoothed__min,B__BVP_HR__Smoothed__variance,B__BVP_IBI_peak_freq._max,B__BVP_IBI_peak_freq._mean,B__BVP_IBI_peak_freq._median,B__BVP_IBI_peak_freq._min,B__BVP_IBI_peak_freq._variance,B__BVP_VLF___power_max,B__BVP_VLF___power_mean,B__BVP_VLF___power_median,B__BVP_VLF___power_min,B__BVP_VLF___power_variance,B__BVP_LF___power_max,B__BVP_LF___power_mean,B__BVP_LF___power_median,B__BVP_LF___power_min,B__BVP_LF___power_variance,B__BVP_HF___power_max,B__BVP_HF___power_mean,B__BVP_HF___power_median,B__BVP_HF___power_min,B__BVP_HF___power_variance,B__BVP_VLF_Total_power_max,B__BVP_VLF_Total_power_mean,B__BVP_VLF_Total_power_median,B__BVP_VLF_Total_power_min,B__BVP_VLF_Total_power_variance,B__BVP_LF_Total_power_max,B__BVP_LF_Total_power_mean,B__BVP_LF_Total_power_median,B__BVP_LF_Total_power_min,B__BVP_LF_Total_power_variance,B__BVP_HF_Total_power_max,B__BVP_HF_Total_power_mean,B__BVP_HF_Total_power_median,B__BVP_HF_Total_power_min,B__BVP_HF_Total_power_variance,C__EMG_+_Smoothing_max,C__EMG_+_Smoothing_mean,C__EMG_+_Smoothing_median,C__EMG_+_Smoothing_min,C__EMG_+_Smoothing_variance,D__EMG_+_Smoothing_max,D__EMG_+_Smoothing_mean,D__EMG_+_Smoothing_median,D__EMG_+_Smoothing_min,D__EMG_+_Smoothing_variance,C_D__C_EMG_-_D_EMG_max,C_D__C_EMG_-_D_EMG_mean,C_D__C_EMG_-_D_EMG_median,C_D__C_EMG_-_D_EMG_min,C_D__C_EMG_-_D_EMG_variance,C_D__C_EMG_+_D_EMG_max,C_D__C_EMG_+_D_EMG_mean,C_D__C_EMG_+_D_EMG_median,C_D__C_EMG_+_D_EMG_min,C_D__C_EMG_+_D_EMG_variance,C_D__EMG_C-D_C+D__balance_fb__max,C_D__EMG_C-D_C+D__balance_fb__mean,C_D__EMG_C-D_C+D__balance_fb__median,C_D__EMG_C-D_C+D__balance_fb__min,C_D__EMG_C-D_C+D__balance_fb__variance,E__SC_as___of_value_max,E__SC_as___of_value_mean,E__SC_as___of_value_median,E__SC_as___of_value_min,E__SC_as___of_value_variance,F__Temp_as___of_value_max,F__Temp_as___of_value_mean,F__Temp_as___of_value_median,F__Temp_as___of_value_min,F__Temp_as___of_value_variance,G__Resp_Amplitude__Abd__max,G__Resp_Amplitude__Abd__mean,G__Resp_Amplitude__Abd__median,G__Resp_Amplitude__Abd__min,G__Resp_Amplitude__Abd__variance,G__Resp_period_max,G__Resp_period_mean,G__Resp_period_median,G__Resp_period_min,G__Resp_period_variance,G__Resp_rate_max,G__Resp_rate_mean,G__Resp_rate_median,G__Resp_rate_min,G__Resp_rate_variance,B_G__HR_max_-_HR_min_max,B_G__HR_max_-_HR_min_mean,B_G__HR_max_-_HR_min_median,B_G__HR_max_-_HR_min_min,B_G__HR_max_-_HR_min_variance,H__Resp_amplitude__thor__max,H__Resp_amplitude__thor__mean,H__Resp_amplitude__thor__median,H__Resp_amplitude__thor__min,H__Resp_amplitude__thor__variance,G_H__Abd_-_Thor_amplitude_diff_max,G_H__Abd_-_Thor_amplitude_diff_mean,G_H__Abd_-_Thor_amplitude_diff_median,G_H__Abd_-_Thor_amplitude_diff_min,G_H__Abd_-_Thor_amplitude_diff_variance,B__BVP_HR_epoch_mean_max,B__BVP_HR_epoch_mean_mean,B__BVP_HR_epoch_mean_median,B__BVP_HR_epoch_mean_min,B__BVP_HR_epoch_mean_variance,B__BVP_IBI_epoch_std_dev_max,B__BVP_IBI_epoch_std_dev_mean,B__BVP_IBI_epoch_std_dev_median,B__BVP_IBI_epoch_std_dev_min,B__BVP_IBI_epoch_std_dev_variance,B__BVP_VLF___power_ep_mean_max,B__BVP_VLF___power_ep_mean_mean,B__BVP_VLF___power_ep_mean_median,B__BVP_VLF___power_ep_mean_min,B__BVP_VLF___power_ep_mean_variance,B__BVP_LF___power_ep_mean_max,B__BVP_LF___power_ep_mean_mean,B__BVP_LF___power_ep_mean_median,B__BVP_LF___power_ep_mean_min,B__BVP_LF___power_ep_mean_variance,B__BVP_HF___power_ep_mean_max,B__BVP_HF___power_ep_mean_mean,B__BVP_HF___power_ep_mean_median,B__BVP_HF___power_ep_mean_min,B__BVP_HF___power_ep_mean_variance,B__BVP_VLF_Total_power_ep_mean_max,B__BVP_VLF_Total_power_ep_mean_mean,B__BVP_VLF_Total_power_ep_mean_median,B__BVP_VLF_Total_power_ep_mean_min,B__BVP_VLF_Total_power_ep_mean_variance,B__BVP_LF_Total_power_ep_mean_max,B__BVP_LF_Total_power_ep_mean_mean,B__BVP_LF_Total_power_ep_mean_median,B__BVP_LF_Total_power_ep_mean_min,B__BVP_LF_Total_power_ep_mean_variance,B__BVP_HF_Total_power_ep_mean_max,B__BVP_HF_Total_power_ep_mean_mean,B__BVP_HF_Total_power_ep_mean_median,B__BVP_HF_Total_power_ep_mean_min,B__BVP_HF_Total_power_ep_mean_variance,B__BVP_LF_HF__ep_means__max,B__BVP_LF_HF__ep_means__mean,B__BVP_LF_HF__ep_means__median,B__BVP_LF_HF__ep_means__min,B__BVP_LF_HF__ep_means__variance,C__EMG_epoch_mean_max,C__EMG_epoch_mean_mean,C__EMG_epoch_mean_median,C__EMG_epoch_mean_min,C__EMG_epoch_mean_variance,D__EMG_epoch_mean_max,D__EMG_epoch_mean_mean,D__EMG_epoch_mean_median,D__EMG_epoch_mean_min,D__EMG_epoch_mean_variance,E__SC_epoch_mean_max,E__SC_epoch_mean_mean,E__SC_epoch_mean_median,E__SC_epoch_mean_min,E__SC_epoch_mean_variance,F__Temp_epoch_mean_max,F__Temp_epoch_mean_mean,F__Temp_epoch_mean_median,F__Temp_epoch_mean_min,F__Temp_epoch_mean_variance,G__Resp_rate_epoch_mean_max,G__Resp_rate_epoch_mean_mean,G__Resp_rate_epoch_mean_median,G__Resp_rate_epoch_mean_min,G__Resp_rate_epoch_mean_variance,B__BVP_amplitude_mean__Rel__max,B__BVP_amplitude_mean__Rel__mean,B__BVP_amplitude_mean__Rel__median,B__BVP_amplitude_mean__Rel__min,B__BVP_amplitude_mean__Rel__variance,B__BVP_HR_mean__beats_min__max,B__BVP_HR_mean__beats_min__mean,B__BVP_HR_mean__beats_min__median,B__BVP_HR_mean__beats_min__min,B__BVP_HR_mean__beats_min__variance,B__BVP_HR_std._dev._max,B__BVP_HR_std._dev._mean,B__BVP_HR_std._dev._median,B__BVP_HR_std._dev._min,B__BVP_HR_std._dev._variance,B__BVP_peak_freq._mean__Hz__max,B__BVP_peak_freq._mean__Hz__mean,B__BVP_peak_freq._mean__Hz__median,B__BVP_peak_freq._mean__Hz__min,B__BVP_peak_freq._mean__Hz__variance,B__BVP_IBI_std._dev.__SDRR__max,B__BVP_IBI_std._dev.__SDRR__mean,B__BVP_IBI_std._dev.__SDRR__median,B__BVP_IBI_std._dev.__SDRR__min,B__BVP_IBI_std._dev.__SDRR__variance,B__BVP_VLF___power_mean_max,B__BVP_VLF___power_mean_mean,B__BVP_VLF___power_mean_median,B__BVP_VLF___power_mean_min,B__BVP_VLF___power_mean_variance,B__BVP_LF___power_mean_max,B__BVP_LF___power_mean_mean,B__BVP_LF___power_mean_median,B__BVP_LF___power_mean_min,B__BVP_LF___power_mean_variance,B__BVP_HF___power_mean_max,B__BVP_HF___power_mean_mean,B__BVP_HF___power_mean_median,B__BVP_HF___power_mean_min,B__BVP_HF___power_mean_variance,B__BVP_VLF_total_power_mean_max,B__BVP_VLF_total_power_mean_mean,B__BVP_VLF_total_power_mean_median,B__BVP_VLF_total_power_mean_min,B__BVP_VLF_total_power_mean_variance,B__BVP_LF_Total_power_mean_max,B__BVP_LF_Total_power_mean_mean,B__BVP_LF_Total_power_mean_median,B__BVP_LF_Total_power_mean_min,B__BVP_LF_Total_power_mean_variance,B__BVP_HF_total_power_mean_max,B__BVP_HF_total_power_mean_mean,B__BVP_HF_total_power_mean_median,B__BVP_HF_total_power_mean_min,B__BVP_HF_total_power_mean_variance,B__BVP_LF_HF__means__max,B__BVP_LF_HF__means__mean,B__BVP_LF_HF__means__median,B__BVP_LF_HF__means__min,B__BVP_LF_HF__means__variance,C__EMG_mean__uV__max,C__EMG_mean__uV__mean,C__EMG_mean__uV__median,C__EMG_mean__uV__min,C__EMG_mean__uV__variance,D__EMG_mean__uV__max,D__EMG_mean__uV__mean,D__EMG_mean__uV__median,D__EMG_mean__uV__min,D__EMG_mean__uV__variance,E__Skin_conductance_mean__uS__max,E__Skin_conductance_mean__uS__mean,E__Skin_conductance_mean__uS__median,E__Skin_conductance_mean__uS__min,E__Skin_conductance_mean__uS__variance,E__SC_as___of_value_mean_____max,E__SC_as___of_value_mean_____mean,E__SC_as___of_value_mean_____median,E__SC_as___of_value_mean_____min,E__SC_as___of_value_mean_____variance,F__Temperature_mean__Deg__max,F__Temperature_mean__Deg__mean,F__Temperature_mean__Deg__median,F__Temperature_mean__Deg__min,F__Temperature_mean__Deg__variance,F__Temp_as___of_value_mean_____max,F__Temp_as___of_value_mean_____mean,F__Temp_as___of_value_mean_____median,F__Temp_as___of_value_mean_____min,F__Temp_as___of_value_mean_____variance,G__Resp_rate_mean__br_min__max,G__Resp_rate_mean__br_min__mean,G__Resp_rate_mean__br_min__median,G__Resp_rate_mean__br_min__min,G__Resp_rate_mean__br_min__variance,B_G___HR_max-min__mean__b_min__max,B_G___HR_max-min__mean__b_min__mean,B_G___HR_max-min__mean__b_min__median,B_G___HR_max-min__mean__b_min__min,B_G___HR_max-min__mean__b_min__variance,G__Abd_amplitude_mean__rel__max,G__Abd_amplitude_mean__rel__mean,G__Abd_amplitude_mean__rel__median,G__Abd_amplitude_mean__rel__min,G__Abd_amplitude_mean__rel__variance,H__Thor_amplitude_mean__rel__max,H__Thor_amplitude_mean__rel__mean,H__Thor_amplitude_mean__rel__median,H__Thor_amplitude_mean__rel__min,H__Thor_amplitude_mean__rel__variance,G_H__Abd-tho_ampl_diff__means__max,G_H__Abd-tho_ampl_diff__means__mean,G_H__Abd-tho_ampl_diff__means__median,G_H__Abd-tho_ampl_diff__means__min,G_H__Abd-tho_ampl_diff__means__variance,B__BVP_IBI_Peak_amplitude_max,B__BVP_IBI_Peak_amplitude_mean,B__BVP_IBI_Peak_amplitude_median,B__BVP_IBI_Peak_amplitude_min,B__BVP_IBI_Peak_amplitude_variance,B__BVP_IBI_Pk_ampl_maximum_max,B__BVP_IBI_Pk_ampl_maximum_mean,B__BVP_IBI_Pk_ampl_maximum_median,B__BVP_IBI_Pk_ampl_maximum_min,B__BVP_IBI_Pk_ampl_maximum_variance,B__BVP_IBI_pk_freq_trigger_max,B__BVP_IBI_pk_freq_trigger_mean,B__BVP_IBI_pk_freq_trigger_median,B__BVP_IBI_pk_freq_trigger_min,B__BVP_IBI_pk_freq_trigger_variance,B__BVP_IBI_pk_ampl_trigger_max,B__BVP_IBI_pk_ampl_trigger_mean,B__BVP_IBI_pk_ampl_trigger_median,B__BVP_IBI_pk_ampl_trigger_min,B__BVP_IBI_pk_ampl_trigger_variance,H__Resp_rate_trigger_max,H__Resp_rate_trigger_mean,H__Resp_rate_trigger_median,H__Resp_rate_trigger_min,H__Resp_rate_trigger_variance,B__BVP_IBI_NN_Intervals_max,B__BVP_IBI_NN_Intervals_mean,B__BVP_IBI_NN_Intervals_median,B__BVP_IBI_NN_Intervals_min,B__BVP_IBI_NN_Intervals_variance,B__BVP_IBI_pNN_Intervals_max,B__BVP_IBI_pNN_Intervals_mean,B__BVP_IBI_pNN_Intervals_median,B__BVP_IBI_pNN_Intervals_min,B__BVP_IBI_pNN_Intervals_variance,B__BVP_IBI_pNN_Intervals_____max,B__BVP_IBI_pNN_Intervals_____mean,B__BVP_IBI_pNN_Intervals_____median,B__BVP_IBI_pNN_Intervals_____min,B__BVP_IBI_pNN_Intervals_____variance,Event_max,Event_mean,Event_median,Event_min,Event_variance,0_max,0_mean,0_median,0_min,0_variance,participant_number,condition_number,emotion_label]
# Do things like detrending...stub for now
def preprocess(data,columns):

	# comment this out to remove detrending
	nrows = data.shape[0]
	for i in range(0,nrows):
		data[:,i] = signal.detrend(data[:,i])
	# / comment

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

			# retrieve columns of CSV from first row
			columns = getColumns(path)

			# preprocess data (things like detrending, etc)
			data = preprocess(raw_data,columns)
			
			# get particpant, condition, and emotion labels
			pn_cn_el = getMeta(path)
			
			# specify features
			featureDict = {
				'mean':np.mean,
				'median':np.median,
				'variance':np.var,
				# 'max':np.max,
				# 'min':np.min,
				# 'fft_f0':
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
