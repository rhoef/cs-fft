"""
randdata.py

Generate random data written to text files
"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'

import numpy as np

def _torecarray(rdata):
    rdata = np.array( zip(rdata, np.arange(rdata.size)),
                      dtype=[("counts", float), ("position", int)])
    rdata = rdata.view(np.recarray)
    return rdata

def white_noise(n, mean=0.0, var=1.0):
    """Return a numpy.recarray with 'counts' and 'position' attributes"""
    rdata = var*np.random.randn(n) + mean
    return _torecarray(rdata)

def intcounts(n, high, low):
    """Return inter samples between high and low inclusive"""
    rdata = np.random.random_integers(high, low, size=n)
    return _torecarray(rdata)

def poission(n, mu):
    rdata = np.random.poisson(mu, n)
    return _torecarray(rdata)

def add_gaps(rarr, ngaps, gap_length=200):
    gpos = np.random.random_integers(0, rarr.size, ngaps)
    glen = np.random.exponential(gap_length, gpos.size)
    glen = np.int_(np.round(glen, 0))

    for p, l in zip(gpos, glen):
        rarr = np.delete(rarr, range(p, p+l))
    return rarr
