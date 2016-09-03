# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:12:58 2016

@author: Cynanthia
"""

import numpy as np
import matplotlib.pyplot as plt

#%%
plt.figure(1)
plt.plot(filtbpf)
plt.title("Filter Kernel for Dataset 2\n(Sampling Frequency = " +
          "256 Hz, Cutoff = 6 and 30 Hz)")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.xlim(0, len(filtbpf)-1)
plt.xticks((0, len(filtbpf)/4, len(filtbpf)/2,
            len(filtbpf)*0.75, len(filtbpf)-1))

#%%
plt.figure(2)
plt.plot(wbpf, 20 * np.log10(hbpf))
plt.title("Frequency Response for Dataset 2's Filter")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.xlim(0, len(wbpf)/4-1)
plt.xticks((0, len(wbpf)/16, len(wbpf)/8,
            len(wbpf)/4*0.75, len(wbpf)/4-1))
