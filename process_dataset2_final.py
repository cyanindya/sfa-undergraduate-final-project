# -*- coding: utf-8 -*-
"""
The script to process the dataset from 'AVI SSVEP Database'
(Adnan Vilic, 2013). The dataset can be downloaded here:
http://www.setzner.com/avi-ssvep-dataset/
"""

# Imports necessary modules
import matplotlib.pyplot as plt
from processEEG.FIRFilterDesign import createFIRFilter as createfilter
import processEEG.processEEGSignal as proc
import numpy as np
import copy  # To implement 'deepcopy' for avoiding dictionary duplication
import csv  # For data writing
import pickle


# Defines the folder where the file exists
fold = str('D:/downloads_unsorted/biomed_refs/EEG-MRI/datasets/BCI/SSVEP/' +
           '(Dataset) AVI SSVEP/AVI_SSVEP_Dataset_MAT/')

#%%
# Create bandpass filter
filtbpf, wbpf, hbpf = createfilter(filtype='bpf', cutoff=[4.0, 15.0], fs=512.0, #BW=4.0
                                   plotkernel=True, plotresponse=True,
                                   amp_dB=True)

#%%
freqresp = np.transpose(np.vstack((wbpf, hbpf)))
np.savetxt('../data/dataset2/20160422/filter/bpf_filt.csv', filtbpf)
np.savetxt('../data/dataset2/20160422/filter/bpf_freqresp.csv', freqresp,
           header='Frequency response\nf (Hz), A (dB)', delimiter=',',
           comments='')

pickle.dump((filtbpf, wbpf, hbpf),
            open('../data/dataset2/20160422/filter/bpf.pkl', 'wb'))

del wbpf, hbpf

#%%
# Generates empty dictionaries to store the processing result.
rawdata = {'s1': {},
           's2': {},
           's3': {},
           's4': {}
           }

filtdata = copy.deepcopy(rawdata)
features = copy.deepcopy(rawdata)

#%%
# Imports the raw signal
for subj in range(1, 5):  # Subject 1-4
    tempdata = proc.extract_rawsignal(fold + 'single/Sub' + str(subj) +
                                      '_singletarget.mat')['Data']

    numtrials = np.shape(tempdata['EEG'][0][0])[1]

    for trial in range(0, numtrials):
        rawdata_temp = (tempdata['EEG'][0][0][:, trial] * 10 ** 6,
                        tempdata['TargetFrequency'][0][0][0][trial])

        rawdata['s' + str(subj)]['T' + str(trial + 1)] = rawdata_temp

        # Timestamp
        t_raw = np.arange(0, len(rawdata_temp[0])/512, 1/512)

        # Writes the extracted signal to csv so it can be processed anytime
        filewrite = np.transpose(np.vstack((t_raw, rawdata_temp[0])))
        csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial + 1) + \
                     ' (' + str(rawdata_temp[1]) + 'Hz)\nt(s), V (uV)'

        np.savetxt('../data/dataset2/20160422/rawdata/s' +
                   str(subj) + 't' + str(trial + 1) + '.csv', filewrite,
                   header=csv_header, delimiter=',', comments='')

pickle.dump(rawdata, open('../data/dataset2/20160422/rawdata/raw_all.pkl',
                          'wb'))

del subj, tempdata, numtrials, trial, rawdata_temp, t_raw, filewrite, csv_header

#%%
# Filter the raw signal
for subj in range(1, 5):  # Subject 1-4

    numtrials = len(rawdata['s' + str(subj)])

    for trial in range(0, numtrials):
        fdata = proc.filterEEG_BPF(rawdata['s' + str(subj)
                                           ]['T' + str(trial + 1)][0], filtbpf)
        fdata = proc.filterEEG_BPF(fdata, filtbpf)
        fdata = proc.filterEEG_BPF(fdata, filtbpf)

        filtdata_temp = (fdata, rawdata['s' + str(subj)]['T' + str(trial + 1)
                                                         ][1])

        filtdata['s' + str(subj)]['T' + str(trial + 1)] = filtdata_temp

        # Timestamp
        t_filt = np.arange(0, len(filtdata_temp[0])/512, 1/512)

        # Writes the extracted signal to csv so it can be processed anytime
        filewrite = np.transpose(np.vstack((t_filt, filtdata_temp[0])))
        csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial + 1) + \
                     ' (' + str(filtdata_temp[1]) + 'Hz)\nt(s), V (uV)'

        np.savetxt('../data/dataset2/20160422/filtdata/s' +
                   str(subj) + 't' + str(trial + 1) + '.csv', filewrite,
                   header=csv_header, delimiter=',', comments='')

pickle.dump(filtdata, open('../data/dataset2/20160422/filtdata/filt_all.pkl',
                           'wb'))

del subj, numtrials, trial, fdata, filtdata_temp, t_filt, filewrite, csv_header

#%%
for subj in range(1, 5):  # Subject 1-4

    numtrials = len(filtdata['s' + str(subj)])

    for trial in range(0, numtrials):
        dat = filtdata['s' + str(subj)]['T' + str(trial + 1)]

        freqresp_temp, maxval_temp = proc.extract_feature(dat[0], fsample=512,
                                                          windowing=True
                                                          )
        features['s' + str(subj)]['T' + str(trial + 1)] = [freqresp_temp,
                                                           maxval_temp,
                                                           dat[1]]
        # Writes the extracted signal to csv so it can be processed anytime
        # filewrite = np.transpose(np.vstack(freqresp_temp))
        filewrite = np.transpose(np.vstack((freqresp_temp[0],
                                            np.abs(freqresp_temp[1]))))
        csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial + 1) + \
                     ' (' + str(dat[1]) + 'Hz)\nf (Hz), V (uV)'

        np.savetxt('../data/dataset2/20160422/features/s' +
                   str(subj) + 't' + str(trial + 1) + '_spect.csv', filewrite,
                   header=csv_header, delimiter=',', comments='')

pickle.dump(features, open('../data/dataset2/20160422/features/features.pkl',
                           'wb'))

del subj, numtrials, trial, dat, freqresp_temp, maxval_temp, filewrite
del csv_header

#%%
# Write the feature extraction result to CSV
csfile = open('../data/dataset2/20160422/features/features_all.csv', 'w',
              newline='')
tmp = csv.writer(csfile, dialect='excel')
tmp.writerow(['Naracoba', 'Trial', 'Frekuensi Target (ftarget)',
              'Hasil FFT (fFFTmax)', 'fFFTmax/ftarget'])

for subj in range(1, 5):  # Subject 1-4

    numtrials = len(rawdata['s' + str(subj)])

    for trial in range(1, numtrials + 1):
        actualfreq = features['s' + str(subj)]['T' + str(trial)][2]
        dat = features['s' + str(subj)]['T' + str(trial)][1][1]
        ratio = dat/actualfreq

        tmp.writerow([subj if (trial == 1) else '', trial, actualfreq, dat,
                      ratio])

csfile.close()

del subj, numtrials, trial, actualfreq, dat, ratio

#%%
# Plot various data
pl = plt.figure(1, figsize=(7.5, 4.5))
ax1 = pl.add_subplot(111)

ax1.plot(np.arange(0, len(filtdata['s1']['T1'][0])/512, 1/512),
         filtdata['s1']['T1'][0])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude ($\mu$V)')
ax1.set_title('''Raw EEG-SSVEP Signal (Subject 1, Trial 10 (6Hz))''')
ax1.grid()

pl.tight_layout()
plt.savefig('sig1.png', dpi=100)


#%%
pl = plt.figure(1, figsize=(7.5, 4.5))
ax1 = pl.add_subplot(111)

ax1.plot(features['s1']['T10'][0][0][:512],
         np.abs(features['s1']['T10'][0][1][:512]))
# plt.xlim((0, 256))
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Amplitude ($\mu$V)')
ax1.set_title('''Frequency Spectrum of EEG-SSVEP Signal
(Subject 1, Trial 10 (6Hz))''')
pl.tight_layout()
plt.savefig('sig1.png', dpi=100)
