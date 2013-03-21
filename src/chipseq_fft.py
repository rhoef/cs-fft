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
import pylab as pl
from matplotlib import mlab
import randdata as rd
from dataprep import DataPrep
from smooth import smooth

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

    bgcounts = np.recfromtxt(bgfile, dtype=int, names=True)
    counts = np.recfromtxt(args.file, names=True, dtype=int)
#    dp.counts[:] = 1

    # counts = rd.poission(100000, 1)
    # bgcounts = rd.poission(100000, 1)
    # counts = rd.add_gaps(counts, 300, 150)

#    bgcounts = rd.add_gabs(bgcounts, 0.47, 50, 0)
#    import pdb; pdb.set_trace()

    dp = DataPrep(counts, bgcounts, crop=args.crop,
                  fill=args.fill, normalize=False)
    dp.gap_stats()

    smoo = dp.counts #smooth(dp.counts, 0)

    fig = pl.figure()
    ax = fig.add_subplot(111)
    npoints = 30000
    idx = range(0, dp.position.size,
                int(max(round(dp.position.size/npoints, 0), 1)))
    ax.set_title("Samples")
    ax.plot(dp.position[idx], smoo[idx], "o-", label="peaks")

    # fig = pl.figure()
    # ax = fig.add_subplot(111)
    # ax.set_title("Power spectrum")
    # pxx, f = ax.psd(dp.counts, Fs=0.1, NFFT=512, noverlap=256)

    # spectram
    # fig = pl.figure()
    # ax = fig.add_subplot(111)
    # ax.specgram(dp.counts, Fs=0.1)

    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Power spectrum")
    pxx, f = mlab.psd(smoo, Fs=0.1, NFFT=512, window=mlab.window_none)
    #ax.plot(f, 10*np.log10(pxx), "x-", label="Power Spectral Density")
    ax.plot(f, pxx, "x-", label="Power Spectral Density")
    # ax.set_xlim((0.0, 5e-5))
    ax.set_xlabel("wave number (1/bp)")
    ax.set_ylabel("power spectral density (dB/bp)")

    # fig = pl.figure()
    # ax = fig.add_subplot(111)
    # ax.set_title("gap lenght ")
    # ax.hist(dp.gap_length, bins=150, normed=True)
    # # ax.bar(np.arange(dp.gap_length.size), dp.gap_length)
    # # ax.plot(dp.gap_position, dp.gap_length, "o")
    # # ax.set_xticks([str(i) for i in dp.gap_position])

    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.set_title("counts (normalized)")
    ax.hist(dp.counts, bins=25, normed=True)


    pl.show()
