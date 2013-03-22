"""
chipseq_fft.py

Fourier analysis of chip sequencing data to find periodig pattern in binding
sites of proteins.
"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'

import argparse
import numpy as np
from matplotlib import mlab
from dataprep import DataPrep
import plots

if __name__ == "__main__":
    parser = argparse.ArgumentParser(\
        description='Spectral analyis of chip-seq data')
    parser.add_argument('file',
                        help='Text/csv file with spatial data')
    parser.add_argument('-b', '--bgfile', dest="bgfile", default=None,
                        help='Test/csv file with background measurement')
    parser.add_argument("--fill", dest="fill", action="store_true",
                        help="Fill missing gaps with zero")
    parser.add_argument('--crop', dest="crop", type=float, default=None,
                        nargs=2,
                        help="Upper and lower array bounds")
    args = parser.parse_args()

    if args.bgfile is None:
        bgfile = args.file.replace(".txt", "_background.txt")
    else:
        bgfile = args.bgfile

    bgcounts = np.recfromtxt(bgfile, comments="#", delimiter="\t", dtype=int,
                             names=True)
    counts = np.recfromtxt(args.file, comments="#", delimiter="\t", names=True,
                           dtype=int)

    dp = DataPrep(counts, bgcounts, crop=args.crop,
                  fill=args.fill, normalize=False)
    dp.gap_stats()

    smoo = dp.counts #smooth(dp.counts, 0)

    plots.samples(dp.position, dp.counts)
    # xlim = (0.0, 5e-5)
    plots.psd(dp.counts, xlim=None, Fs=0.1, NFFT=512, window=mlab.window_none)
    plots.counts(dp.counts, bins=50, normed=True)
#    plots.gaps(dp.gap_position, dp.gap_length, bins=100, normed=True)
    plots.show()
