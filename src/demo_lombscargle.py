"""
demo_lombscargle.py
"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'

import numpy as np
from matplotlib import mlab
from dataprep import LombScargle
import plots

f1 = 5.
f2 = 10.
pi2 = 2*np.pi
srate = 100

x = np.arange(0, 20, 1./srate)
x0 = np.random.permutation(x)[:10*srate]
x0 = np.sort(x0)
yfunc = lambda t, w1, w2: np.sin(w1*t) + np.sin(w2*t)
y = yfunc(x, f1*pi2, f2*pi2)
y0 = yfunc(x0, f1, f2)

fmin = 1./x.size # = delta_f
fmax = srate/2.0

f = np.arange(1, 50, 0.5, dtype=float)

lb = LombScargle(x0, y0, f)
f, pgram = lb()

plots.samples(x0, y0, window_title="Data Series")
plots.samples(f, pgram, window_title="Lomb-Scargle Periodigram")
plots.psd(y, Fs=srate, NFFT=y.size,
          window_title="Welch Periodigram",
          window=mlab.window_none)
plots.show()
