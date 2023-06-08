import numpy as np
from Fisher import correlation_matrix

import unittest

# python -m pytest test_corr.py 

class TestCorr(unittest.TestCase):
    def test_correlation(self):
        S11 = 6.222
        S22 = 10.889
        S33 = 2.667
        S44 = 17.556
        S12 = 7.778
        S13 = -1.333
        S14 = 8.444
        S23 = -3.333
        S24 = 7.889
        S34 = 2.

        s11 = np.sqrt(S11)
        s22 = np.sqrt(S22)
        s33 = np.sqrt(S33)
        s44 = np.sqrt(S44)

        COR = np.array(((S11/(s11*s11))))

        dats = np.array(((4, 8, 2), (6, 9, 1), (3, 5, 7), (0, 10, 3)))
        m = correlation_matrix(dats)

        assert m[1][1] - S11