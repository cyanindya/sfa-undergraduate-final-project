# -*- coding: utf-8 -*-

# For using in PowerShell, set system encoding to utf-8 first
# $env:PYTHONIOENCODING = "utf-8" (temporary)
# [Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")

# import sys
# import locale
# import os
import processor_dataset_1_1 as pr1

# print(sys.stdout.encoding)
# print(sys.stdout.isatty())
# print(locale.getpreferredencoding())
# print(sys.getfilesystemencoding())
# print(os.environ['PYTHONIOENCODING'])

fold = 'D:/downloads_unsorted/biomed_refs/EEG-MRI/datasets/BCI/SSVEP/(Dataset) AVI SSVEP/AVI_SSVEP_Dataset_CSV/single/'

def exp_1():
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[21])
    pr1.main(fold + 'Sub3_singletarget_EEG.dat', trial=[16])
    pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[23])
    pr1.main(fold + 'Sub4_singletarget_EEG.dat', trial=[17])
    pr1.main(fold + 'Sub3_singletarget_EEG.dat', trial=[1])
    pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[2])
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[24])
    pr1.main(fold + 'Sub4_singletarget_EEG.dat', trial=[1])

def exp_2():
    pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[24])
    pr1.main(fold + 'Sub3_singletarget_EEG.dat', trial=[17])
    pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[19])
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[26])
    pr1.main(fold + 'Sub4_singletarget_EEG.dat', trial=[1])
    pr1.main(fold + 'Sub3_singletarget_EEG.dat', trial=[2])
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[1])
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[23])

def exp_3():
    # pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[2])
    # pr1.main(fold + 'Sub4_singletarget_EEG.dat', trial=[0])
    pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[21], plot_filtered=True, plot_frequency=True)
    pr1.main(fold + 'Sub3_singletarget_EEG.dat', trial=[18], plot_filtered=True, plot_frequency=True)
    pr1.main(fold + 'Sub2_singletarget_EEG.dat', trial=[22], plot_filtered=True, plot_frequency=True)
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[25], plot_filtered=True, plot_frequency=True)
    pr1.main(fold + 'Sub1_singletarget_EEG.dat', trial=[22], plot_filtered=True, plot_frequency=True)
    # pr1.main(fold + 'Sub3_singletarget_EEG.dat', trial=[2])


# exp_1()
# exp_2()
exp_3()

