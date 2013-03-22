"""
gentestdata.py

Generate test data for testing

e.g.
python gentestdata.py -n 200000 -p 1000 -c 10 -g 5000 -l 100 -b 1.5 -f testdata.txt

"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'

import sys
import argparse
import numpy as np
import pylab as pl

def write_files(filename, position, counts, delimiter='\t'):
    # data file
    with open(filename, "w") as fp:
        # fp.write('# '+" ".join(sys.argv))
        # fp.write('\n')
        fp.write('''"position"%s"counts\n''' %delimiter)
        for pos, count in zip(positions, counts):
            fp.write("%d%s%d\n" %(pos, delimiter, count))

    # background measurement
    with open(filename.replace(".txt", "_background.txt"), "w") as fp:
        # fp.write('# '+" ".join(sys.argv))
        # fp.write('\n')
        fp.write('''"position"%s"counts\n''' %delimiter)
        for pos in positions:
            fp.write("%d%s1\n" %(pos, delimiter))


def add_counts(counts, lambda_, ratio):
    while True:
        pos = np.random.randint(0, counts.size)
        length = 10 + np.random.poisson(1)
        # import pdb; pdb.set_trace()
        height = np.int_(np.random.exponential(lambda_))
        # height = np.random.poisson(1)
        counts[pos:pos+length] += height

        if float(counts[counts==0].size)/counts.size < (1-ratio):
            break
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(\
        description='Generate test data for testing')
    parser.add_argument('-f', '--file', dest='file',
                        help=("Output file (background measurement derives "
                              "automatically)"))
    parser.add_argument('--plot', action='store_true',
                        help='Plots the data')
    parser.add_argument('-n', '--nsamples', dest="nsamples", default=100,
                        type=int, help='Number of samples (default=10000)')
    parser.add_argument('-r' '--ratio', dest='ratio', type=float, default=0.2,
                        help=("Rel. amount of background (default=0.2%%"))
    parser.add_argument('-p', '--peaks-ratio', dest='pratio', type=float,
                        default=0.01,
                        help='Amount of peaks (default=0.01%%)')
    parser.add_argument('-b', '--background', dest='background', type=float,
                        default=0.25,
                        help="Default background (mean of an exponential dist.)")
    parser.add_argument('-t', '--pheight', dest='pheight', type=float,
                        default=10.0,
                        help="Default peak-height (mean of an exponential dist.)")
    args = parser.parse_args()

    # empty arrays
    positions = np.arange(0, args.nsamples, 10, dtype=int)
    counts = np.zeros(positions.shape, dtype=int)


    # add some peaks
    counts = add_counts(counts, args.pheight, ratio=args.pratio)
    # fill with background
    counts = add_counts(counts, args.background, ratio=args.ratio)


    if args.plot:
        fig = pl.figure()
        ax = fig.add_subplot(111)
        ax.plot(positions, counts, 'b')
        ax.set_ylabel("counts")
        ax.set_xlabel('position')
        pl.show()
    else:
        positions = sorted(positions)
        #func = lambda positions: positions
        #counts = sorted(counts, key=func)
        write_files(args.file, positions, counts)
