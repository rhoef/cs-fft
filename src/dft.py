#!/usr/bin/python

import numpy as np
import pylab as pl

f1 = 1
f2 = 3.33333
pi2 = 2.0*np.pi
srate=20.

t = np.arange(0, 500., 1./srate)
y = np.ones(t.shape)
y[t<20] = 0
y[t>20.1] = 0
# y = np.sin(f1*t*pi2) + np.sin(pi2*f2*t)

fy = np.fft.fft(y, n=y.size+100)
psd = abs(fy)*2/fy.size
freq = np.fft.fftfreq(t.size, 1/srate)

pl.figure('Signal')
pl.plot(t, y, 'o-')

pl.figure('fft')
idx = freq>0
pl.plot(freq[idx], psd[idx],'xr-')
pl.show()
