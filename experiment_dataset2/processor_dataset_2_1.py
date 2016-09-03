# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 23:47:38 2016

@author: Cynanthia
"""

# Import necessary modules and functions
import sys
import time

sys.path.append('..')

import matplotlib.pyplot as plt
import processEEG.processEEGSignal as proc
import numpy as np
import csv
import pickle
import argparse
import serial

def main(filename, channels=[14, 20, 22, 27], port='COM5', plot_raw=False,
         plot_filtered=False, plot_frequency=False):
    
    chs = channels
    rawfile = filename

    # Extracts raw signal from file
    rawdata = np.transpose(proc.extract_rawsignal(rawfile).get('EEGdata')[chs])
    t_raw = np.arange(0, len(rawdata)/256, 1/256)
    t_raw = np.reshape(t_raw, (len(t_raw), 1))
    
    print('\nSignal file ' + rawfile + ' opened. Now processing...')
    
    # Retrieves filter kernel
    with open('bpf_filt.csv', 'r') as filtin:
        filtfile = csv.reader(filtin, delimiter='\n')
        
        bpf_filt = []
        
        for row in filtfile:
            bpf_filt.append(row[0])
    
    bpf_filt = np.array(bpf_filt)
    bpf_filt = bpf_filt.astype(float)
    
    # Filters raw data
    print('Filtering signal...')
    
    filtdata = proc.filterEEG_BPF(rawdata, bpf_filt)
    filtdata = proc.filterEEG_BPF(filtdata, bpf_filt)
    filtdata = proc.filterEEG_BPF(filtdata, bpf_filt)
    
    t_filt = np.arange(0, len(filtdata)/256, 1/256)
    t_filt = np.reshape(t_filt, (len(t_filt), 1))
    
    # Deletes unwanted signal segment
    print('Cleaning unwanted signal chunks...')
    
    segment = proc.segmentsignal(filtdata, fsample=256.0, duration=15, kill=[4.5, 4.5], space=0)
    
    # Extract frequency spectrum and its maximum value
    print('Performing FFT algorithm...')
    
    ft = []
    for ch in range(0, len(chs)):
    
        freqresp_temp, maxval_temp = proc.extract_feature(segment[:, ch], fsample=256.0, windowing=True)
        ft.append([freqresp_temp, maxval_temp[1]])
    
    
    features = np.array([ft[0][1], ft[1][1], ft[2][1], ft[3][1]]).reshape(1, -1)
    
    print('Detected peak frequency array: %s Hz. Now classifying using SVM...' % np.array_str(features[0]))
    
    # Predicst feature output
    classifier = pickle.load(open('svm_classifier.pkl', 'rb'))[0]
    
    out = classifier.predict(features)
    
    print('SVM classification completed. Detected target device: LED #%i.' % out[0])
    
    # For debugging purposes only
    # print(rawdata)
    # print(t_raw)
    # print(filtdata)
    # print(segment)
    
    print('Attempting to connect to the plant...')
    
    try:
        outport = serial.Serial()
        outport.setDTR(value=0)  # Disables DTR to prevent Arduino auto-reset
        outport.port = 'COM5'
        outport.baudrate = 9600
        outport.timeout = 2.0
    #    outport.dtr = 0  # For PySerial 3.0+ replacing setDTR
        outport.open()
        
        print('Connection to plant through %s successful. Now sending data...' % outport.port)
        
    except serial.serialutil.SerialException:
        print('Connection to plant failed. Skipping data transmission process.\n')
    
    if ('outport' in locals()) and outport.is_open:
        outport.write(b'%i' % out[0])
        outport.close()
        
        print('Data transmission successful.\n')
    
    if plot_raw:
        rawplot = plt.figure(num=0)
        rawplot_0 = rawplot.add_subplot(111)
        rawplot_0.plot(t_raw, rawdata)
        rawplot_0.set_xlim(0, t_raw[-1])
    
        rawplot_0.set_title("Raw Signal")
        rawplot_0.set_xlabel("Time (s)")
        rawplot_0.set_ylabel("Amplitude ($\mu$V)")
        rawplot.tight_layout()
    
    if plot_filtered:
        filtplot = plt.figure(num=1)
        filtplot_0 = filtplot.add_subplot(111)
        filtplot_0.plot(t_filt, filtdata)
        filtplot_0.set_xlim(0, t_filt[-1])
    
        filtplot_0.set_title("Filtered Signal")
        filtplot_0.set_xlabel("Time (s)")
        filtplot_0.set_ylabel("Amplitude ($\mu$V)")
        filtplot.tight_layout()
    
    if plot_frequency:
        fftplot = plt.figure(num=2)
        fftplot_0 = fftplot.add_subplot(111)
        for i in range(0, len(chs)):
            fftplot_0.plot(ft[i][0][0], np.abs(ft[i][0][1]))
        fftplot_0.set_xlim(0, 35)
    
        fftplot_0.set_title("Frequency Spectrum")
        fftplot_0.set_xlabel("Frequency (Hz)")
        fftplot_0.set_ylabel("Amplitude ($\mu$V)")
        fftplot.tight_layout()
    
    if plot_raw or plot_filtered or plot_frequency:
        print('Printing specified signal plots...\n')
        plt.show()
    else:
        time.sleep(3)
