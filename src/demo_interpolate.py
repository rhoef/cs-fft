"""
demo_interpolate.py
"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'


from dataprep import Spline
import numpy as np
from pylab import *
from scipy.interpolate import splev, splrep

srate = 50

x = np.arange(0, 20, 1./srate)
x0 = np.random.permutation(x)[:20*50]
x0 = np.sort(x0)
y0 = np.sin(2*np.pi*5*x0)


spline = Spline(x0, y0, k=3)
y = spline(x)

freq = np.fft.fftfreq(y.size, 1./srate)
ffty = abs(np.fft.fft(y))*2/y.size

figure("Fft")
fi = freq > 0

plot(freq[fi], ffty[fi], 'rx-')

figure("Interpolation Demo")
plot(x0, y0, "x")

plot(x, y, 'r-')
tck = splrep(x0, y0)
y = splev(x, tck)
plot(x, y, 'g-')

show()
