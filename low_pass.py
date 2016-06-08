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

import matplotlib.pyplot as plt
import datetime
import numpy as np
import sys
import columns
import filters

def main():
	col = columns.Columns()
	
	print('Reading data...')

	data = np.loadtxt(sys.argv[1], dtype=float, delimiter=',', skiprows=9)
	
	sc = data[:,col.selectColumn('E: Skin Cond')] # skin conductivity
	scf = filters.lowpass(2,0.01,sc)
	scd = filters.detrend(scf)

	# Make plots
	fig = plt.figure(1)

	ax1 = fig.add_subplot(211)
	plt.plot(range(0,sc.size),sc, 'b-')
	plt.plot(range(0,sc.size),scf, 'r-',linewidth=2)
	plt.plot(range(0,sc.size),scd, 'g-',linewidth=2)
	ax1.axes.get_xaxis().set_visible(False)

	ax1 = fig.add_subplot(212)
	plt.plot(range(0,sc.size),sc-scf, 'b-')
	

	sp = np.fft.fft(sc)
	freq = np.fft.fftfreq(sc.shape[-1])
	plt.figure(2)
	plt.plot(freq, sp.real, freq, sp.imag)

	plt.show()



if __name__ == "__main__":
	print('Argument List:', str(sys.argv))
	if (len(sys.argv) > 1):
		main()