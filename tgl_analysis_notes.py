################################################################################
##<---------------------------- 80 chars across ----------------------------->##
##        1         2         3         4         5         6         7       ##  
##2345678901234567890123456789012345678901234567890123456789012345678901234567##
#------------------------------------------------------------------------------#
################################################################################
''' 
# Biophysical Emotion detection algorithms in Python

Paul Bucci
pbucci@cs.ubc.ca

## References: 

+ Emotion Recognition Based on Physiological Changes in Music Learning
 
## Signals

### ECG

#### Features

+ Heart rate (HR)
++ Differentiate between postive and negative emotions
+ Heart rate variability (HRV)
++ Oscilation of the interval between consecutive hearbeats
++ Indicator of mental effort and stress
+ Interbeat interval (IBI)

### Respiration

#### Features

+ Respiration rate (RSP)
++ Decreases with relaxation
++ Startling and tense moments may briefly stop respiration
++ Negative emotions cause irregularity in RSP 
++ Coupled with SC and EMG 

### Skin conductivity

#### Features

+ Skin conductivity (SC)
++ Slow-moving tonic component for temperature and other influences
++ Fast phasic component for emotions/level of arousal

## Methods

### Preprocessing

+ Low pass filtering for noise (all signals)

### Measured Features

#### ECG

+ Subband spectrum --> FFT
++ 

'''

from scipy import signal
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import datetime
import numpy as np
import sys

class Columns:
	def __init__(self):
		self.columns = ['Time','B: BVP','C: EMG','D: EMG','E: Skin Cond','F: Temp','G: Abd Resp','H: Thor Resp (optional)','B: BVP amplitude','B: BVP IBI','B: BVP HR from IBI','B: BVP HR (Smoothed)','B: BVP IBI peak freq.','B: BVP VLF % power','B: BVP LF % power','B: BVP HF % power','B: BVP VLF Total power','B: BVP LF Total power','B: BVP HF Total power','C: EMG + Smoothing','D: EMG + Smoothing','C&D: C:EMG - D:EMG','C&D: C:EMG + D:EMG','C&D: EMG C-D/C+D (balance fb)','E: SC as % of value','F: Temp as % of value','G: Resp Amplitude (Abd)','G: Resp period','G: Resp rate','B&G: HR max - HR min','H: Resp amplitude (thor)','G&H: Abd - Thor amplitude diff','B: BVP HR epoch mean','B: BVP IBI epoch std dev','B: BVP VLF % power ep mean','B: BVP LF % power ep mean','B: BVP HF % power ep mean','B: BVP VLF Total power ep mean','B: BVP LF Total power ep mean','B: BVP HF Total power ep mean','B: BVP LF/HF (ep means)','C: EMG epoch mean','D: EMG epoch mean','E: SC epoch mean','F: Temp epoch mean','G: Resp rate epoch mean','B: BVP amplitude mean (Rel)','B: BVP HR mean (beats/min)','B: BVP HR std. dev.','B: BVP peak freq. mean (Hz)','B: BVP IBI std. dev. (SDRR)','B: BVP VLF % power mean','B: BVP LF % power mean','B: BVP HF % power mean','B: BVP VLF total power mean','B: BVP LF Total power mean','B: BVP HF total power mean','B: BVP LF/HF (means)','C: EMG mean (uV)','D: EMG mean (uV)','E: Skin conductance mean (uS)','E: SC as % of value mean (%)','F: Temperature mean (Deg)','F: Temp as % of value mean (%)','G: Resp rate mean (br/min)','B&G: (HR max-min) mean (b/min)','G: Abd amplitude mean (rel)','H: Thor amplitude mean (rel)','G&H: Abd-tho ampl diff (means)','B: BVP IBI Peak amplitude','B: BVP IBI Pk ampl maximum','B: BVP IBI pk freq trigger','B: BVP IBI pk ampl trigger','H: Resp rate trigger','B: BVP IBI NN Intervals','B: BVP IBI pNN Intervals','B: BVP IBI pNN Intervals (%)']
	
	def getColumns(self):
		return self.columns

	def searchColumns(self,sterm):
		return [x for x in self.columns if x.find(sterm) > -1]

	def selectColumn(self,sterm):
		ret = self.searchColumns(sterm)
		if len(ret) == 1:
			ind = ret[0]
			i = 0
			for j in self.columns:
				if j == ind:
					return i
				i = i + 1
			return (-1)
		else:
			return (-1)


## lowpass --------------------------------------------------------------------#
# Create a FIR filter and apply it to x.
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
#
# X is vector to filter
# n is length of vector
# sample_rate is the sample rate
# thz = transition width
# rdb = ripple_db
# cutoff_hz = The cutoff frequency of the filter.

# thz example: 
#  cutoff_hz = 200hz
#  thz       = 20hz
#     --> filter will start attenuating at 180hz for a soft
#         attenuation and finish at 200hz (note that this 
#         is inevitable in continous signals)
def lowpass(X,n,sample_rate,cutoff_hz=10.0,thz=5.0,rdb=60.0):
	# The Nyquist rate of the signal (note: always half).
	nyq_rate = sample_rate / 2.0

	# The desired width of the transition from pass to stop,
	# relative to the Nyquist rate.  We'll design the filter
	# with a 5 Hz transition width.
	width = thz/nyq_rate

	# The desired attenuation in the stop band, in dB.
	ripple_db = rdb

	# Compute the order and Kaiser parameter for the FIR filter.
	N, beta = kaiserord(ripple_db, width)

	# Use firwin with a Kaiser window to create a lowpass FIR filter.
	taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

	# Use lfilter to filter x with the FIR filter.
	filtered_X = lfilter(taps, 1.0, X)

	return filtered_X

# http://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html?highlight=butter

def plotting(x,y,n):
	plt.figure(n)
	plt.plot(x,y)

#fs is sample rate
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def main():
	col = Columns()
	
	print('Reading data...')

	data = np.loadtxt(sys.argv[1], dtype=float, delimiter=',', skiprows=9)
	


	# print(data.shape)
	
	sc = data[:,col.selectColumn('E: Skin Cond')] # skin conductivity
	

	# First, design the Buterworth filter
	N  = 2    # Filter order
	Wn = 0.01 # Cutoff frequency
	B, A = signal.butter(N, Wn, output='ba')

	# Second, apply the filter
	scf = signal.filtfilt(B,A, sc)

	# Make plots
	fig = plt.figure(1)
	ax1 = fig.add_subplot(211)
	plt.plot(range(0,sc.size),sc, 'b-')
	plt.plot(range(0,sc.size),scf, 'r-',linewidth=2)
	plt.ylabel("Temperature (oC)")
	plt.legend(['Original','Filtered'])
	plt.title("Temperature from LOBO (Halifax, Canada)")
	ax1.axes.get_xaxis().set_visible(False)

	ax1 = fig.add_subplot(212)
	plt.plot(range(0,sc.size),sc-scf, 'b-')
	plt.ylabel("Temperature (oC)")
	plt.xlabel("Date")
	plt.legend(['Residuals'])

	# import matplotlib.pyplot as plt
	# t = np.arange(256)
	sp = np.fft.fft(sc)
	freq = np.fft.fftfreq(sc.shape[-1])
	plt.figure(2)
	plt.plot(freq, sp.real, freq, sp.imag)
	# plt.show()

	# plotting(range(0,sc.size),sc,1)
	
	# print("filtering....")

	# filtered_data = butter_bandpass_filter(data,0.01,0.05,1)

	# print("Done filtering.")
	
	# print("Plotting.")

	# plotting(range(0,sc.size),filtered_data,2)

	plt.show()



if __name__ == "__main__":
	print('Argument List:', str(sys.argv))
	if (len(sys.argv) > 1):
		main()