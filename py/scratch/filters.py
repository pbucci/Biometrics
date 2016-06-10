# Module is simple signal processing functions
from scipy import signal
from scipy.signal import butter, lfilter
# N  = Filter order
# Wn = Cutoff frequency)
def lowpass(N,Wn,data):
	# First, design the Buterworth filter
	B, A = signal.butter(N, Wn, output='ba')

	# Second, apply the filter
	dataf = signal.filtfilt(B,A, data)
	return dataf

# fs is sample rate
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Just a wrapper for this function:
# http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.signal.detrend.html
# right now, leaving parameters out
def detrend(data): # axis=-1,type='linear',bp=0):
	return signal.detrend(data)