# -*- coding: utf-8 -*-
"""
The module containing the basic functions for EEG signal processing.
"""

#%%
# Imports necessary NumPy and SciPy modules' functions
import numpy as np
import scipy.signal as sig
import scipy.io as sio
from scipy.fftpack import fft  # , ifft


#%%
# The function to extract raw data.
# Inputs: - The file containing raw EEG data (txt, csv, mat)
#         - The list of channels. Note that because the 0th
#           column contains 'ticks', specify the number of channels
#           as usual (eg. [2, 4] for data in channels 2 and 4)
def extract_rawsignal(inputdata, channels=[]):

    # Reads file type first. Note that -3:-1 doesn't include
    # the very last character so we have to add it ourselves.
    ftype = inputdata[-3:-1] + inputdata[-1]

    # Loads the EEG data acquired.
    if ftype in ['txt', 'csv', 'dat']:
        # Read OpenBCI data
        if 'OpenBCI' in open(inputdata).read():
            rawdata = np.loadtxt(inputdata, comments='%', delimiter=', ')
        else:
            rawdata = np.loadtxt(inputdata, delimiter=',')

        # TODO: smooth out the code to read non-OpenBCI files
    elif ftype == 'mat':  # Matlab .mat file
        rawdata = sio.loadmat(inputdata)
    else:
        raise Exception("File type not recognized.")

    # Removes unnecessary data. If no channel numbers are
    # unspecified, all data will be extracted (default).
    # Otherwise, only data from specified channels will be carried
    # over.
    # TODO: non-OpenBCI data handling (since they end up turning differently.)
    if not channels:
        if (ftype in ['txt', 'csv']) and ('OpenBCI' in open(inputdata,
                                                 'r').read()):
            # Kills all data in column 0, which only indicates the
            # data 'ticks'.
            rawdata = rawdata[:, 1:]
        else:
            pass
    else:
        rawdata = rawdata[:, channels]

    return rawdata


#%%
# TODO: The function to filter extracted data using BPF.
# Because we want to separate frequencies and not concerned about
# speed, windowed-sinc FIR filter is used.
# Inputs: - The array of raw data to be processed
#         - Sampling frequency of the signal (Hz).
#         - Cut-off frequencies (fc1 and fc2) in Hz.
# TODO: Should we use a pre-existing filter or let the design take
# place inside the function?
# TODO: Custom filter. Right now we only use pre-made filter.
def filterEEG_BPF(rawdata, filt, channels=[]):  # ,fsample=250.0, cutoff=[]):

    # Convolve the filter kernel
    if channels:
        if np.size(channels) >= 2:
            filtdata = np.empty([len(rawdata) + len(filt) - 1, len(channels)])

            for i in range(0, np.shape(filtdata)[1]):
                for ch in channels:
                    filtdata_temp = sig.fftconvolve(rawdata[:, ch], filt)

                    filtdata[:, i] = filtdata_temp
        else:
            filtdata = sig.fftconvolve(rawdata[:, channels[0]], filt)
    else:
        if np.size(np.shape(rawdata)) >= 2:
            filtdata = np.empty([len(rawdata) + len(filt) - 1,
                                 np.shape(rawdata)[1]])

            for ch in range(0, np.shape(rawdata)[1]):
                filtdata_temp = sig.fftconvolve(rawdata[:, ch], filt)

                filtdata[:, ch] = filtdata_temp
        else:
            filtdata = sig.fftconvolve(rawdata, filt)

    filtdata = filtdata[len(filt)//2-1:-len(filt)//2]

    return filtdata
    # return filtdata_temp


#%%
# The function to segment the pre-processed data into
# smaller pieces before feature extraction.
# Inputs: - The array of filtered data to be segmented
#         - Sampling frequency of the signal (Hz).
#         - Duration of each segment in seconds
#         - Duration of the signal's "tails" to be omitted
# TODO: segmentation when there are spaces between the observed segments.
#       (eg. like in P300 experiment)
def segmentsignal(filtdata, fsample=250.0, duration=0.0, kill=[1.0, 1.0],
                  space=0.0):

    # Truncate the signal's tails
    killsample = np.array(kill) * fsample
    filtdata = filtdata[killsample[0]:-killsample[1]-1]

    # Segment the signal
    # Defines the signal length and space between segments in samples
    length = fsample * duration

    # Calculates each segment's starting point, taking account of the
    # spaces between each segment
    start = np.arange(0, len(filtdata), length + space * fsample)

    # Creates an empty array to save the segmentation results
    segments = []

    # Breaks the input into segments. If the segment length is shorter
    # than it's supposed to be (e.g. 'leftover' data), don't store it.
    for i in range(0, len(start)):
        temp = filtdata[start[i]:start[i] + length]

        if len(temp) >= length:
            segments.append(temp)
            # return temp
    
    # If only one signal exists, kill segment
    if len(segments) < 2:
        segments = segments[0]

    # Returns the stored segments' container as output.
    return segments


#%%
# The function to extract features of the filtered data.
# Because we want to see the SSVEP frequency, FFT is used.
# Inputs: - The data segment to be transformed.
#         - Sampling frequency of the segment (Hz).
#         - Is windowing enabled?
# TODO: Why is the result abnormally huge when compared to OpenBCI
#       FFT?
# Make sure the segment length equals the sampling rate!
def extract_feature(seg, fsample=250.0, windowing=False):

    N = len(seg)

    # Calculate the nearest power of 2 number
    pow2 = 0
    NFFT = 0

    while (N > np.power(2, pow2)):
        pow2 += 1

        if N <= np.power(2, pow2):
            NFFT = np.power(2, pow2)
            break

    # Do single-channel FFT...
    if windowing:  # runs this line if windowing is enabled
        window = sig.blackman(N, sym=False)

        fft_result = fft(seg * window, n=NFFT)
    else:  # otherwise, run this one
        fft_result = fft(seg, n=NFFT)

    # ...and calculate the frequency spacing of the sample.
    # Remember, unlike real DFT, the frequency of complex DFT
    # ranges from 0.0 to 1.0 of sampling frequency!
    # freq spacing (delta-f) = fsample / N(FFT)
    fspacing = np.linspace(0.0, fsample, NFFT)

    # Returns the highest absplute amplitude calculated along
    # its origin frequency
    fmaxval = (np.max(np.abs(fft_result[1:len(fft_result)/2-1])),
               np.argmax(np.abs(fft_result[1:len(fft_result)/2-1])) /
               len(fft_result) * fsample)
#    fmaxval = (np.max(np.abs(fft_result[N//fsample:len(fft_result)/2-1])),
#               np.argmax(np.abs(fft_result[N//fsample:len(fft_result)/2-1])) /
#               len(fft_result) * fsample)

    # TODO: FFT on all channels, and then search for max value.
    # fftseg = []

    # for i in len(seg[0]):
    #     fftseg[i] = fft(seg[i])

    # fftseg = np.array(fftseg)

    return (fspacing, fft_result), fmaxval


#%%
# TODO: The function to plot processed data
