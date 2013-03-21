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
        fp.write('''"position"%s"counts\n''' %args.delimiter)
        for pos, count in zip(positions, counts):
            fp.write("%d%s%d\n" %(pos, args.delimiter, count))

    # background measurement
    with open(filename.replace(".txt", "_background.txt"), "w") as fp:
        # fp.write('# '+" ".join(sys.argv))
        # fp.write('\n')
        fp.write('''"position"%s"counts\n''' %args.delimiter)
        for pos in positions:
            fp.write("%d%s1\n" %(pos, args.delimiter))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(\
        description='Generate test data for testing')
    parser.add_argument('-f', '--file', dest='file',
                        help=("Output file (background measurement derives "
                              "automatically)"))
    parser.add_argument('--plot', action='store_true',
                        help='Plots the data')
    parser.add_argument('-n', '--nsamples', dest="nsamples", default=10000,
                        type=int,
                        help='Number of samples (default=10000)')
    parser.add_argument('-s', '--start', dest='start', default=0, type=int,
                        help="Start position (default=0)")
    parser.add_argument('-g', '--ngaps', dest='ngaps', type=int, default=50,
                         help="Number of gaps in %% of nsamples (default=50)")
    parser.add_argument('-l', '--length', dest='length', type=int, default=10,
                        help=("Mean gap length, base on an exponential dist. "
                              "(default=50))"))
    parser.add_argument('-p', '--npeaks', dest='npeaks', type=int, default=50,
                        help='Number of peaks (default=50)')
    parser.add_argument('-c', '--height', dest='height', type=int, default=85,
                        help='Mean peak height (default=185)')
    parser.add_argument('-b', '--background', dest='mean_background', type=float,
                        default=2,
                        help=(('Mean background, base on a poisson dist. '
                               '(default=3)')))
    parser.add_argument('-d', '--delimiter', default='\t', dest='delimiter',
                        type=str,
                        help='delimiter')
    args = parser.parse_args()

    # noisy background
    positions = np.arange(0, args.nsamples, 1, dtype=int)
    counts = np.random.exponential(args.mean_background, positions.size)
    counts = np.int_(np.round(counts, 0))

    # delete data supposed to represent the gaps
    gpos = np.random.permutation(positions)[:args.ngaps]
    gidx = []
    glen = np.int_(np.random.exponential(round(args.length), size=gpos.size))
    for pos, length in zip(gpos, glen):
        gidx.extend(range(pos, pos+length, 1))

    positions = np.delete(positions, gidx)
    counts = np.delete(counts, gidx)

    # add some random peaks
    pheight = np.int_(np.random.exponential(round(args.height), size=args.npeaks))
    if args.nsamples < args.npeaks:
        raise ValueError("Number of samples must be larger than number of peaks")
    if pheight.size > counts.size:
        import pdb; pdb.set_trace()
        raise ValueError("Array must be larger than number of peaks")
    counts[:args.npeaks] = pheight
    np.random.shuffle(counts)

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
        write_files(args.file, positions, counts, args.delimiter)
