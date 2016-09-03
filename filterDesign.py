# -*- coding: utf-8 -*-
"""
The file specifically used for filter design. May turn into
a function later.
"""

#%%
# Imports the signal and plot stuffs
import numpy as np
import scipy.signal as sig
from scipy.fftpack import fft
import matplotlib.pyplot as plt


#%%
# Defines the 'regular' values
fs = 256.0  # Hz
fc1 = 6.0  # Hz
fc2 = 35.0  # Hz
nyqf = fs / 2  # Hz
BW = 4.0  # Hz

# Defines the fractioned values, if fs (250 Hz) is 1.0
fc1_frac = fc1 / fs
fc2_frac = fc2 / fs
BW_frac = BW / fs
nyq_frac = nyqf / fs

# Computes the filter kernel length (M = 4/BW); BW is in fraction.
M = 4.0 / BW_frac


#%%
# Design windowed-sinc FIR filter using 'regular' values
filt = sig.firwin(M, fc2, width=BW, window='blackman', nyq=nyqf)

#%%
# Design windowed-sinc FIR filter using fractioned/normalized values
# (that is, with Nyquist frequency being 0.5 of sampling frequency)
# filt = sig.firwin(M, fc2_frac, width=BW_frac, window='blackman',
#                  pass_zero=True, nyq=nyq_frac)  # LPF, proto-HPF
filt = sig.firwin(M, [fc1_frac, fc2_frac], width=BW_frac, window='blackman',
                  pass_zero=False, nyq=nyq_frac)  # BPF, proto-notch

#%%
# Convert LPF to HPF manually.
filt = filt * np.sin(2 * np.pi * nyqf * np.linspace(0, 1, fs))  # sp-reversal
filt = 0 - filt  # sp-inversion
filt[M/2] += 1.0

#%%
# Computes the frequency response of the generated filter.
# TODO: why is the result different between regular FFT and freqz?
# Shortcut (in normalized rad/sample form)
w, h = sig.freqz(filt)
w = w * fs / (2 * np.pi)  # de-normalize if you wish
h = np.abs(h)

#%%
# Computes frequency response manually through z-transform
# Basically freqz() decomposed. Learn!
# z = e^wj
w = np.linspace(0, np.pi, len(filt) * 2)  # How many frequencies to evaluate?
n = np.array(range(0, len(filt)))  # filter's sample index [n]

H = []  # generates an empty array for storing calculation result

for i in w:  # for every frequency listed in w...
    h = np.sum(filt * np.exp(-1j * i * n))  # b[0] + b[1] * e ^ (-j1 * i * n)

    H.append(h)

H = np.array(H)
H_abs = np.abs(H)

#%%
# Long way using FFT (convert the Hz frequency to radian then divide by total
# sample, then compute the frequency spectrum).
w = np.linspace(0, len(filt), fs)
# w = np.linspace(0, len(filt), fs) * 2 * np.pi / len(filt)  # normalized
h = np.abs(fft(filt))
w = w[:M/2]  # only take the lower half
h = h[:M/2]

#%%
# Long way by calculating manually. This is only to understand
# how exactly the time -> frequency conversion works, not for long-
# term implementation.
# TODO: why is the amplitude half of the regular FFT method when the real
# and imaginary components of the frequencies are not multiplied by 2?

# Generates empty list to store the real and imaginary values.
ReFilt = []
ImFilt = []

# Defines variables for calculation results for one sample in frequency
# domain
cs = 0
sn = 0

# Calculates the real and imaginary value of one time-domain sample
# in frequency domain.
for k in range(0, len(filt)//2 + 1):  # freq, remember, k length is N/2!
    for i in range(0, len(filt)):  # time
        # Calculates sine and cosine value of one time-domain sample
        # for the current freq-domain sample
        pnt_cos = filt[i] * np.cos(2 * np.pi * k * i / len(filt))
        pnt_sin = filt[i] * np.sin(2 * np.pi * k * i / len(filt))

        # Adds the previous calculation of time-domain samples with
        # current time-domain sample
        cs += pnt_cos
        sn += pnt_sin

    # Appends the fully-summed calculation result to the lists
    ReFilt.append(cs)
    ImFilt.append(-sn)

# Converts the list into arrays
ReFilt = 2 * np.array(ReFilt)
ImFilt = 2 * np.array(ImFilt)

# Calculates the magnitude of the kernel for each sample point
MagFilt = (ReFilt ** 2.0 + ImFilt ** 2.0) ** 0.5

# converts the magnitude list to array
MagFilt = np.array(MagFilt)

#%%
# Converts magnitude from standard uV(?) to dB
h = 20.0 * np.log10(np.abs(h))

#%%
# Plots the frequency response.
plt.plot(w, h)
# plt.plot(w[:len(w)/2], h[:len(h)/2])  # divide by two, don't forget!
plt.title('Frequency Response of the Filter')
plt.xlabel('Frequency [Hz]')
# plt.xlabel(u'Normalized Frequency [x \u03C0 rad/sample]')
plt.ylabel('Amplitude')

#%%
# Deletes unneeded variables to clear up memory.
# Use var = None instead if you want to reference the variable(s) later.
del fs, fc1, fc2, nyqf, BW, fc1_frac, fc2_frac, BW_frac, nyq_frac, M
del cs, sn, pnt_cos, pnt_sin, i, k
