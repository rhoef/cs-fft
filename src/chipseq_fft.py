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
from dataprep import DataPrep, LombScargle
import plots


class ConflictHandler(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        if option_string.strip("-") == "fill":
            namespace.fill = True
        else:
            namespace.fill = False

        if option_string.strip("-") == "lomb-scargle":
            if namespace.welch is True:
                raise RuntimeError("Cannot perform both periodigrams in one run")
            namespace.lomb_scargle = True
            namespace.welch = False
            namespace.fill = False

        elif option_string.strip('-') == "welch":
            if namespace.lomb_scargle is True:
                raise RuntimeError("Cannot perform both periodigrams in one run")
            namespace.lomb_scargle = False
            namespace.welch = True

class FileAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        namespace.file = values
        namespace.bgfile = values.replace('.txt', '_background.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(\
        description='Spectral analyis of chip-seq data.')
    parser.add_argument('file', action=FileAction,
                        help='Text/csv file with spatial data.')
    parser.add_argument('-b', '--bgfile', dest="bgfile", default=None,
                        help='Test/csv file with background measurement.')
    parser.add_argument("--fill", dest="fill", action=ConflictHandler,
                        nargs=0,
                        help="Fill missing gaps with zeros.")
    parser.add_argument('--crop', dest="crop", type=float, default=None,
                        nargs=2,
                        help="Upper and lower array bounds.")
    parser.add_argument('--frange', dest="frange", type=float, default=None,
                        nargs=2,
                        help="Frequency limits for the plots.")
    parser.add_argument('--lomb-scargle', dest="lomb_scargle", nargs=0,
                        action=ConflictHandler,
                        help="Plots a lomb scargle periodigram.")
    parser.add_argument('--welch', dest="welch", action=ConflictHandler,
                        nargs=0, help='Plot a welche periodigram.')
    parser.add_argument('--nfft', dest='nfft', type=int, default=256,
                        help="Window size for the Welch periodigram.")

    args = parser.parse_args()


    bgcounts = np.recfromtxt(args.bgfile, comments="#", delimiter="\t",
                             dtype=int, names=True)
    counts = np.recfromtxt(args.file, comments="#", delimiter="\t", names=True,
                           dtype=int)

    dp = DataPrep(counts, bgcounts, crop=args.crop,
                  fill=args.fill, normalize=False)
    dp.gap_stats()

    if args.lomb_scargle:
        # calculate the LombScargle Periodigram in the
        # frequency range of interessest
        freq_ls = np.linspace(5.0e-7, 5.0e-4, 500)
        ls = LombScargle(np.float_(dp.position), np.float_(dp.counts), freq_ls)
        f, pgram = ls()
        ax = plots.samples(f, pgram, window_title="Lomb-Scargle Periodigram")
        ax.semilogy()

    if args.welch:
        plots.samples(dp.position, dp.counts, window_title="Raw data")
        # xlim = (0.0, 5e-5)
        fs = np.diff(dp.position).min()
        plots.psd(dp.counts, xlim=args.frange, Fs=fs, NFFT=args.nfft,
                  window=mlab.window_none,
                  window_title="Welch Periodigram")
        plots.samples(dp.position, dp.counts, window_title="Raw data")
        plots.show()
