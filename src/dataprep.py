"""
dataprep.py

"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'

import numpy as np
from scipy.stats.mstats import zscore


class DataPrep(object):

    def __init__(self, data, bgdata, crop=None, fill=False, normalize=True):
        super(DataPrep, self).__init__()

        self.gap_position = None
        self.gap_length = None
        self._data = data
        self._bgdata = bgdata

        dmin = data.position.min()
        self.position = data.position.copy() - dmin
        self.counts = data.counts.copy()

        if crop is not None:
            if len(crop) != 2:
                raise ValueError(("Cropping parameter requires a sequence "
                                  "of lenght 2"))
            self._crop(*crop)

        if normalize:
            self.counts = zscore(self.counts)

        if fill:
            self._fill_missing()

        if self.gap_length is None:
            self._gap_lenght(self.position)

    def _normalize(self):
        self.counts = zscore(self.counts)

    def _crop(self, xmin, xmax):
        mask = ((self.position>=xmin)*(self.position<=xmax))
        self.position = self.position[mask]
        self.counts = self.counts[mask]

        if self.counts.size == 0:
            raise RuntimeError("No samples left after cropping")

    def gap_stats(self):
        """Print some array statistics of the croped and filled data."""

        pos = self._data.position
        bgpos = self._bgdata.position
        union = np.unique(np.append(pos, bgpos))
        union = union[(union>=pos.min()*(union<=pos.max()))]
        union = np.sort(union)

        print "x min: ", self.position.min()
        print "x max: ", self.position.max()
        ratio = float(union.size - pos.size)/union.size
        print "Rel. amount of gaps: %.2f%%" %(100.0*ratio)

        # use mean from an expoential distribution
        print "Mean gap length: ", self.gap_length.mean()

        print "Size of array: ", union.size
        print "Number of gaps: ", self.gap_length.size
        if self.gap_length.size > 0:
            print "Max gap size: ", self.gap_length.max()

    def _gap_lenght(self, position):
        # indices of the array not the values
        delta = np.diff(position).min()
        x_ind = (position - position.min())/delta
        diff = np.diff(x_ind)
        self.gap_length = (diff[diff>1] - 1)*delta
        self.gap_position = np.arange(x_ind.size, dtype=int)[diff>1]

    def _fill_missing(self, gap_value=0):

        # indices of the array not the values
        delta = np.diff(self.position).min()
        x_ind = (self.position - self.position.min())/delta

        x0 = np.arange(self.position.min(), self.position.max()+delta,
                       delta, dtype=self.position.dtype)

        y0 = np.ones(x0.size)*gap_value
        y0[x_ind] = self.counts

       # print float(self.counts/y0)

        self._gap_lenght(self.position)

        self.position = x0
        self.counts = y0
