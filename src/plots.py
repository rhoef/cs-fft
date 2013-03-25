"""
plots.py
"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'


import pylab as pl
from matplotlib import mlab

def show():
    pl.show()

def samples(position, counts, window_title=111):
    fig = pl.figure(window_title)
    ax = fig.add_subplot(111)
    npoints = 30000
    idx = range(0, position.size,
                int(max(round(position.size/npoints, 0), 1)))
    ax.set_title("Samples")
    ax.plot(position[idx], counts[idx], "o-", label="peaks")
    return ax

def psd(counts, exclude_zero=True, xlim=None, window_title=111,
        *args, **kw):
    fig = pl.figure(window_title)
    ax = fig.add_subplot(111)
    ax.set_title("Power spectrum")
    pxx, f = mlab.psd(counts, *args, **kw)
    #ax.plot(f, 10*np.log10(pxx), "x-", label="Power Spectral Density")
    if exclude_zero:
        pxx, f = pxx[1:], f[1:]
    ax.plot(f, pxx, "x-", label="Power Spectral Density")
    if xlim is not None:
        ax.set_xlim((0.0, 5e-5))
    ax.semilogy(True)
    ax.set_xlabel("wave number (1/bp)")
    ax.set_ylabel("power spectral density (counts/bp)")
    return ax

def counts(counts, window_title=111, *args, **kw):
    fig = pl.figure(window_title)
    ax = fig.add_subplot(111)
    ax.set_title("counts (normalized)")
    ax.hist(counts, *args, **kw)
    return ax

def spectgram(counts, fs=1, window_title=111):
    fig = pl.figure(window_title)
    ax = fig.add_subplot(111)
    ax.specgram(counts, Fs=fs)
    return ax

def psd2(counts, window_title=111, *args, **kw):
    """Default function from matplotlib."""
    fig = pl.figure(window_title)
    ax = fig.add_subplot(111)
    ax.set_title("Power spectrum")
    pxx, f = ax.psd(counts, *args, **kw)
    return ax

def gaps(gaps_pos, gap_length, window_title=111, *args, **kw):
    fig = pl.figure(window_title)
    ax = fig.add_subplot(111)
    ax.set_title("gap lenght")
    ax.hist(gap_length, *args, **kw)
    # ax.bar(np.arange(dp.gap_length.size), dp.gap_length)
    # ax.plot(dp.gap_position, dp.gap_length, "o")
    # ax.set_xticks([str(i) for i in dp.gap_position])
