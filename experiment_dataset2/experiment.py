# -*- coding: utf-8 -*-

# For using in PowerShell, set system encoding to utf-8 first
# $env:PYTHONIOENCODING = "utf-8" (temporary)
# [Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")

# import sys
# import locale
# import os
import processor_dataset_2_1 as pr2

# print(sys.stdout.encoding)
# print(sys.stdout.isatty())
# print(locale.getpreferredencoding())
# print(sys.getfilesystemencoding())
# print(os.environ['PYTHONIOENCODING'])

fold = 'D:/downloads_unsorted/biomed_refs/EEG-MRI/datasets/BCI/SSVEP/(Dataset) Optimization of SSVEP brain responses with application to eight-command Brain–Computer Interface/'

def exp_1():
    pr2.main(fold + 'S1/SSVEP_8Hz_Trial1_SUBJ1.mat')
    pr2.main(fold + 'S1/SSVEP_14Hz_Trial1_SUBJ1.mat')
    pr2.main(fold + 'S2/SSVEP_14Hz_Trial2_SUBJ2.mat')
    pr2.main(fold + 'S2/SSVEP_8Hz_Trial3_SUBJ2.mat')
    pr2.main(fold + 'S3/SSVEP_28Hz_Trial1_SUBJ3.mat')
    pr2.main(fold + 'S3/SSVEP_14Hz_Trial2_SUBJ3.mat')
    pr2.main(fold + 'S4/SSVEP_28Hz_Trial3_SUBJ4.mat')
    pr2.main(fold + 'S4/SSVEP_28Hz_Trial4_SUBJ4.mat')

def exp_2():
    pr2.main(fold + 'S1/SSVEP_14Hz_Trial4_SUBJ1.mat')
    pr2.main(fold + 'S2/SSVEP_8Hz_Trial2_SUBJ2.mat')
    pr2.main(fold + 'S1/SSVEP_14Hz_Trial1_SUBJ1.mat')
    pr2.main(fold + 'S3/SSVEP_28Hz_Trial3_SUBJ3.mat')
    pr2.main(fold + 'S4/SSVEP_28Hz_Trial5_SUBJ4.mat')
    pr2.main(fold + 'S2/SSVEP_8Hz_Trial3_SUBJ2.mat')
    pr2.main(fold + 'S4/SSVEP_8Hz_Trial3_SUBJ4.mat')
    pr2.main(fold + 'S4/SSVEP_8Hz_Trial1_SUBJ4.mat')

def exp_3():
    pr2.main(fold + 'S2/SSVEP_28Hz_Trial2_SUBJ2.mat')
    pr2.main(fold + 'S3/SSVEP_8Hz_Trial1_SUBJ3.mat')
    pr2.main(fold + 'S1/SSVEP_14Hz_Trial3_SUBJ1.mat')
    pr2.main(fold + 'S4/SSVEP_14Hz_Trial4_SUBJ4.mat')
    pr2.main(fold + 'S2/SSVEP_28Hz_Trial3_SUBJ2.mat')
    pr2.main(fold + 'S4/SSVEP_8Hz_Trial2_SUBJ4.mat')
    pr2.main(fold + 'S3/SSVEP_14Hz_Trial5_SUBJ3.mat')
    pr2.main(fold + 'S1/SSVEP_14Hz_Trial3_SUBJ1.mat')


# exp_1()
# exp_2()
# exp_3()
pr2.main(fold + 'S1/SSVEP_28Hz_Trial2_SUBJ1.mat', plot_raw=True, plot_filtered=True, plot_frequency=True)

