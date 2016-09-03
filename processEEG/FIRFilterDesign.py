# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:21:46 2016

@author: Cynanthia
"""

# Imports the signal and plot stuffs
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt


# Defines the function to create FIR filter
def createFIRFilter(filtype='lpf', cutoff=1.0, fs=250.0, BW=4.0, **kwargs):
    """
    Create a FIR-type digital filter for given parameters.

    Usage:
    ------
    filt, w, h = createFIRFilter(...)
    filt = createFIRFilter(...)[0]
    w, h = createFIRFilter(...)[1, 2]

    with:
        filt - the resulting filter kernel/impulse response
        w - the filter's frequency range either in radian or Hz
        h - the filter's magnitude either in decimal or dB

    Parameters:
    -----------
    filtype: string
        The filter type to be designed.

        'lpf' - low-pass filter (default)
        'hpf' - high-pass filter
        'bpf' - band-pass filter
        'notch' - band-reject/notch filter

    cutoff: float
        The cutoff frequency where the filter will operate in Hz.
        Default value is 1 Hz.

        For band-pass and notch filters, specify the 'cutoff' as a list
        containing the lower and upper cutoff frequencies, e.g. [1, 30]

    fs: float
        The sampling frequency of the signal to be filtered in Hz.
        Default value is 250 Hz.

    BW: float
        The length of filter's transitional bandwidth in Hz.
        Default value is 4 Hz.


    Additional parameters:
    ----------------------
    window: string
        The window to be used for the filter. Defaults to Blackman
        ('blackman') window.

        See the documentation of scipy.signal.firwin() for the details
        of available windows.

    frequnit: string
        The frequency unit we're working on. Note that this is only for
        frequency response-plotting purpose; the filter creation still
        uses the Hertz unit.

        'Hz' - Hertz (default)
        'rad' - radian

    normalize: bool
        If True, plots the filter's response in normalized (rad/sample)
        frequency. Defaults to False.

    amp_dB: bool
        If True, plots the filter's frequency response in dB unit, otherwise
        in decimal. Defaults to False.

    plotkernel: bool
        If True, plots the filter's impulse response. Defaults to False.

    plotresponse: bool
        If True, plots the filter's frequency response. Defaults to False.

    TODO: plots the step response
    """

    # (Yes, it's probably better to just specify them in the function's
    # definition in the first place, but they'll end up cluttering the
    # function's definition.)
    #
    # See if the specified keyword arguments are present when the function
    # is called. Otherwise, return default values for them.
    win = kwargs.get('window', 'blackman')
    frequnit = kwargs.get('frequnit', 'Hz')
    normalize = kwargs.get('normalize', False)

    # Based on the inputs, define the Nyquist frequency and the transition
    # bandwidth in fractional form.
    nyquist = fs / 2

    BW_frac = BW / fs
    nyq_frac = nyquist / fs

    # Defines the filter length (filter order + 1)
    M = 4.0 / BW_frac

    # Checks which type of filter is to be designed, then create it.
    if filtype in ['lpf', 'hpf']:
        # Specifies the cutoff frequency in fractional form
        cutoff_frac = cutoff / fs

        # Create low-pass filter.
        if filtype == 'lpf':
            filt = sig.firwin(M, cutoff_frac, width=BW_frac, window=win,
                              pass_zero=True, nyq=nyq_frac)

        # Create high-pass filter.
        else:
            # Spectral inversion causes the frequency response to go haywire
            # for some reasons. Use spectral reversal instead - which means
            # the raw LPF is actually designed at (nyquist - intended cutoff)
            filt = sig.firwin(M, nyq_frac - cutoff_frac, width=BW_frac,
                              window=win, pass_zero=True, nyq=nyq_frac)

            # Spectral inversion
            # filt = -filt
            # filt[int(M)/2] = filt[M/2] + 1.0

            # Spectral reversal
            filt = filt * np.sin(2 * np.pi * nyquist * np.linspace(0, 1, fs))

    elif filtype in ['bpf', 'notch']:
        # Raise exception if the supposed lower cutoff is same as or
        # higher than upper cutoff
        if (cutoff[0] >= cutoff[1]):
            raise Exception("""Lower cutoff frequency must be smaller
                            than upper cutoff.""")

        # Specifies the lower and upper cutoff frequencies in fractional form
        fc1_frac = cutoff[0] / fs
        fc2_frac = cutoff[1] / fs

        # Create band-pass filter
        if filtype == 'bpf':
            filt = sig.firwin(M, [fc1_frac, fc2_frac], width=BW_frac,
                              window=win, pass_zero=False,
                              nyq=nyq_frac)

        # Create notch/band-reject filter.
        # Spectral reversal cannot be used directly on band-pass filter for
        # some reason, so we create two separate low-pass and high-pass filters
        # instead before combining them.
        else:
            filt_low = sig.firwin(M, fc1_frac, width=BW_frac, window=win,
                                  pass_zero=True, nyq=nyq_frac)
            filt_high = sig.firwin(M, nyq_frac - fc2_frac, width=BW_frac,
                                   window=win, pass_zero=True, nyq=nyq_frac)

            filt_high = filt_high * np.sin(2 * np.pi * nyquist *
                                           np.linspace(0, 1, fs))

            filt = filt_low + filt_high

    else:
        raise Exception("Unknown filter type")

    # Computes the frequency response of the generated filter.
    # w = the frequency range to be evaluated, from 0 to pi
    # h = filter magnitude
    # Normal (freqz) way
    # Out: normalized [rad/sample] freq, amplitude
    w, h = sig.freqz(filt)

    # If we wish the frequency to be shown in Hz...
#    if frequnit == 'Hz':
#        w = w * fs / (2 * np.pi)
#    # ...or in rad, but no normalization
#    elif (frequnit == 'rad') and not normalize:
#        w = w / (2 * np.pi) * len(filt)
    # End of normal way

    # Long way
    # It's better to calculate frequency response in 2^x form,
    # so we'll check the closest power of 2 value that is larger than
    # the filter length
    pow2 = 0
    length = len(filt)

    while (length > np.power(2, pow2)):
        pow2 += 1

        if length <= np.power(2, pow2):
            length = np.power(2, pow2)
            break

    # How many frequencies to test?
    w = np.linspace(0, np.pi, length * 2)

    # filter's sample index [n]
    n = np.array(range(0, len(filt)))

    # generates an empty array for storing calculation result
    h = []

    for i in w:  # for every frequency listed in w...
        # amplitude of each sample
        htemp = np.sum(filt * np.exp(-1j * i * n))

        h.append(htemp)

    # Converts the resulting amplitude calculation into array
    h = np.array(h)

    # Is the frequency to be plotted in Hz?
    if frequnit == 'Hz':
        w = w * fs / (2 * np.pi)
    # Or in normalized rad?
    elif (frequnit == 'rad') and normalize:
        w = w / (2 * np.pi)
    else:
        pass
    # End of long way

    h = np.abs(h)

    if kwargs.get('plotkernel', False) or kwargs.get('plotresponse', False):

        if filtype in ['bpf', 'notch']:
            co = '%d and %d' % (cutoff[0], cutoff[1])

            if filtype == 'bpf':
                tp = 'Band-Pass'
            else:
                tp = 'Notch'
        else:
            co = cutoff

            if filtype == 'lpf':
                tp = 'Low-Pass'
            else:
                tp = 'High-Pass'

    if kwargs.get('amp_dB', False):
        h = 20 * np.log10(h)

    if kwargs.get('plotkernel', False):
        f1 = plt.figure(num=0, figsize=(7.5, 4.5))
        kern = f1.add_subplot(111)

        kern.plot(filt)

        kern.set_xlabel("Sample Number")
        kern.set_ylabel("Amplitude")
        kern.set_xlim((0, len(filt)))

        kern.set_title('Filter Impulse Response\n' + '(%d Hz, %s at %s Hz)'
                       % (fs, tp, co))
        f1.tight_layout()

    if kwargs.get('plotresponse', False):
        f2 = plt.figure(num=1, figsize=(7.5, 4.5))
        resp = f2.add_subplot(111)
        resp.plot(w[1:-1], h[1:-1])

        if (frequnit == 'rad'):
            if normalize:
                resp.set_xlabel("Normalized Frequency (rad/sample)")
            else:
                resp.set_xlabel("Frequency (rad)")
        else:
            resp.set_xlabel("Frequency (Hz)")
            resp.set_xlim((0, fs/2))
            resp.set_xticks(np.linspace(0, fs/2-1, 5))

        if kwargs.get('amp_dB', False):
            resp.set_ylabel("Amplitude [dB]")
        else:
            resp.set_ylabel("Amplitude")

        resp.set_title('Filter Frequency Response\n' + '(%d Hz, %s at %s Hz)'
                       % (fs, tp, co))
        f2.tight_layout()

    return filt, w, h
