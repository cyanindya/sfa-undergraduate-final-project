# -*- coding: utf-8 -*-
"""
The script to process the dataset from 'Optimization
of SSVEP brain responses with application to eight-command
Brain–Computer Interface' (Bakardjian H, Tanaka T, Cichocki A,
2010). The dataset can be downloaded here: http://www.bakardjian.com/
work/ssvep_data_Bakardjian.html.
"""

import matplotlib.pyplot as plt
from processEEG.FIRFilterDesign import createFIRFilter as createfilter
import processEEG.processEEGSignal as proc
import numpy as np
import copy  # To implement 'deepcopy' for avoiding dictionary duplication
import csv
import pickle

#%%
fold = str('D:/downloads_unsorted/biomed_refs/EEG-MRI/datasets/BCI/SSVEP/' +
           '(Dataset) Optimization of SSVEP brain responses with application' +
           ' to eight-command Brain–Computer Interface/')

freqs = ['8', '14', '28']
chs = [14, 20, 22, 27]  # because using 128 channels at once is overkill

#%%
# Create bandpass filters
filtbpf, wbpf, hbpf = createfilter(filtype='bpf', cutoff=[6.0, 30.0], fs=256.0,
                                   plotkernel=True, plotresponse=True,
                                   amp_dB=True)

#%%
freqresp = np.transpose(np.vstack((wbpf, hbpf)))
np.savetxt('../data/dataset1/20160422/common/filter/bpf_filt.csv', filtbpf)
np.savetxt('../data/dataset1/20160422/common/filter/bpf_freqresp.csv',
           freqresp, header='Frequency response\nf (Hz), A (dB)',
           delimiter=',', comments='')

pickle.dump((filtbpf, wbpf, hbpf),
            open('../data/dataset1/20160422/common/filter/bpf.pkl', 'wb'))

del wbpf, hbpf

#%%
# Generates empty dictionaries to store the processing result.
rawdata = {'s1': {'8Hz': {'T1': None,
                          'T2': None,
                          'T3': None,
                          'T4': None,
                          'T5': None
                          },
                  '14Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           },
                  '28Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           }
                  },
           's2': {'8Hz': {'T1': None,
                          'T2': None,
                          'T3': None,
                          'T4': None,
                          'T5': None
                          },
                  '14Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           },
                  '28Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           }
                  },
           's3': {'8Hz': {'T1': None,
                          'T2': None,
                          'T3': None,
                          'T4': None,
                          'T5': None
                          },
                  '14Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           },
                  '28Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           }
                  },
           's4': {'8Hz': {'T1': None,
                          'T2': None,
                          'T3': None,
                          'T4': None,
                          'T5': None
                          },
                  '14Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           },
                  '28Hz': {'T1': None,
                           'T2': None,
                           'T3': None,
                           'T4': None,
                           'T5': None
                           }
                  }
           }

filtdata = copy.deepcopy(rawdata)
segments = copy.deepcopy(rawdata)
features = copy.deepcopy(rawdata)

#%%
for subj in range(1, 5):  # Subject 1-4
    for frq in freqs:
        for trial in range(1, 6):  # Trial 1-5
            rawdata_temp = np.transpose(proc.extract_rawsignal(
                                        fold + 'S' + str(subj) + '/SSVEP_' +
                                        frq + 'Hz_Trial' + str(trial) +
                                        '_SUBJ' + str(subj) + '.mat'
                                        ).get('EEGdata')[chs])
            # rawdata[subj-1][freqs.index(frq)].append(rawdata_temp)
            rawdata['s' + str(subj)][frq + 'Hz']['T' +
                                                 str(trial)] = rawdata_temp

            t = np.arange(0, len(rawdata_temp)/256, 1/256)
            t = np.reshape(t, (len(t), 1))

            filewrite = np.hstack((t, rawdata_temp))
            csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial) +\
                         ' (' + frq + 'Hz)\nt(s), O1 (uV), POz (uV),' + \
                         ' Oz (uV), O2 (uV)'

            np.savetxt('../data/dataset1/20160422/common/rawdata/s' +
                       str(subj) + '_' + frq + 'Hz_t' + str(trial) + '.csv',
                       filewrite, header=csv_header, delimiter=',',
                       comments='')

pickle.dump(rawdata,
            open('../data/dataset1/20160422/common/rawdata/raw_all.pkl',
                 'wb'))
del subj, frq, trial, t, filewrite, csv_header, rawdata_temp

#%%
for subj in range(1, 5):  # Subject 1-4
    for frq in freqs:
        for trial in range(1, 6):  # Trial 1-5
            filtdata_temp = proc.filterEEG_BPF(rawdata['s' + str(subj)]
                                               [frq + 'Hz']['T' + str(trial)],
                                               filtbpf)

            # Cascade the BPF to suppress the DC frequency as much as
            # possible
            filtdata_temp = proc.filterEEG_BPF(filtdata_temp, filtbpf)
            filtdata_temp = proc.filterEEG_BPF(filtdata_temp, filtbpf)

            filtdata['s' + str(subj)][frq + 'Hz']['T' +
                                                  str(trial)] = filtdata_temp

            t = np.arange(0, len(filtdata_temp)/256, 1/256)
            t = np.reshape(t, (len(t), 1))

            filewrite = np.hstack((t, filtdata_temp))
            csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial) +\
                         ' (' + frq + 'Hz)\nt(s), O1 (uV), POz (uV),' + \
                         ' Oz (uV), O2 (uV)'

            np.savetxt('../data/dataset1/20160422/common/filtdata/s' +
                       str(subj) + '_' + frq + 'Hz_t' + str(trial) + '.csv',
                       filewrite, header=csv_header, delimiter=',',
                       comments='')

pickle.dump(filtdata,
            open('../data/dataset1/20160422/common/filtdata/filt_all.pkl',
                 'wb'))

del subj, frq, trial, t, filewrite, csv_header, filtdata_temp

#%%
for subj in range(1, 5):  # Subject 1-4
    for frq in freqs:
        for trial in range(1, 6):  # Trial 1-5
            segment_temp = proc.segmentsignal(filtdata['s' + str(subj)][frq +
                                              'Hz']['T' + str(trial)],
                                              fsample=256.0, duration=15,
                                              kill=[4.5, 4.5], space=0)
            segments['s' + str(subj)][frq + 'Hz']['T' +
                                                  str(trial)] = segment_temp

            t = np.arange(0, len(segment_temp)/256, 1/256)
            t = np.reshape(t, (len(t), 1))

            filewrite = np.hstack((t, segment_temp))
            csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial) +\
                         ' (' + frq + 'Hz)\nt(s), O1 (uV), POz (uV),' + \
                         ' Oz (uV), O2 (uV)'

            np.savetxt('../data/dataset1/20160422/common/segments/s' +
                       str(subj) + '_' + frq + 'Hz_t' + str(trial) + '.csv',
                       filewrite, header=csv_header, delimiter=',',
                       comments='')

#pickle.dump(segments,
#            open('../data/dataset1/20160422/common/segments/seg_all.pkl',
#                 'wb'))

del subj, frq, trial, t, filewrite, csv_header, segment_temp

#%%
for subj in range(1, 5):  # Subject 1-4
    for frq in freqs:
        for trial in range(1, 6):  # Trial 1-5
            lis = []
            for chan in range(0, len(chs)):
                freqresp_temp, maxval_temp = proc.extract_feature(
                                                    segments['s' + str(subj)]
                                                    [frq + 'Hz']
                                                    ['T' + str(trial)]
                                                    [:, chan], fsample=256,
                                                    windowing=True)
                lis.append([freqresp_temp, maxval_temp])

            features['s' + str(subj)][frq + 'Hz']['T' + str(trial)] = lis

            filewrite = np.transpose(np.vstack((lis[0][0][0], lis[0][0][1],
                                                lis[1][0][1], lis[2][0][1],
                                                lis[3][0][1])))
            csv_header = 'Subject' + str(subj) + ', Trial ' + str(trial) +\
                         ' (' + frq + 'Hz)\nf (Hz), O1 (uV), POz (uV),' + \
                         ' Oz (uV), O2 (uV)'

            np.savetxt('../data/dataset1/20160422/common/features/s' +
                       str(subj) + '_' + frq + 'Hz_t' + str(trial) +
                       '_spect.csv', filewrite, header=csv_header,
                       delimiter=',', comments='')

#pickle.dump(features,
#            open('../data/dataset1/20160422/common/features/fft_all.pkl',
#                 'wb'))

del subj, frq, trial, chan, lis, filewrite, csv_header, freqresp_temp
del maxval_temp


#%%
# Write frequency response to CSV
csfile = open('../data/dataset1/20160422/common/features/features_all.csv',
              'w', newline='')
tmp = csv.writer(csfile, dialect='excel')
tmp.writerow(['Naracoba', 'Frekuensi Target', 'Trial', 'Hasil FFT (O1)',
              'Hasil FFT (POz)', 'Hasil FFT (Oz)', 'Hasil FFT (O2)'])

for subj in range(1, 5):  # Subject 1-4
    for frq in freqs:
        for trial in range(1, 6):  # Trial 1-5
            dat_O1 = features['s' + str(subj)][frq + 'Hz'
                                               ]['T' + str(trial)][0][1][1]
            dat_POz = features['s' + str(subj)][frq + 'Hz'
                                                ]['T' + str(trial)][1][1][1]
            dat_Oz = features['s' + str(subj)][frq + 'Hz'
                                               ]['T' + str(trial)][2][1][1]
            dat_O2 = features['s' + str(subj)][frq + 'Hz'
                                               ]['T' + str(trial)][3][1][1]

            tmp.writerow([subj if (frq == freqs[0] and (trial == 1)) else '',
                         int(frq) if (trial == 1) else '', trial, dat_O1,
                         dat_POz, dat_Oz, dat_O2])

csfile.close()

del subj, frq, trial, dat_O1, dat_POz, dat_Oz, dat_O2

#%%
pl = plt.figure(1, figsize=(7.5, 4.5))
ax1 = pl.add_subplot(111)

ax1.plot(np.arange(0, len(rawdata['s1']['8Hz']['T2'][:, 0])/256, 1/256),
         rawdata['s1']['8Hz']['T2'][:, 0])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude ($\mu$V)')
ax1.set_title('''Raw EEG-SSVEP Signal (Subject 1, 8Hz, Trial 2, O1)''')
ax1.grid()

pl.tight_layout()
plt.savefig('sig11.png', dpi=100)


#%%
# Plot various data
pl = plt.figure(1, figsize=(7.5, 4.5))
ax1 = pl.add_subplot(111)

ax1.plot(features['s1']['8Hz']['T2'][0][0][0][:640],
         np.abs(features['s1']['8Hz']['T2'][0][0][1][:640]))
# plt.xlim((0, 256))
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Amplitude ($\mu$V)')
ax1.set_title('''Frequency Spectrum of EEG-SSVEP Signal
(Subject 1, 8Hz, Trial 2, O1)''')
plt.savefig('sig2.png', dpi=100)