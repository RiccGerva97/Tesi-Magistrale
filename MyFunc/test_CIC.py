import numpy as np
from myCIC import cic

import unittest

class TestCIC(unittest.TestCase):
    def test_density(self):
        points = np.array(((7.5, 7.5, 7.5), (0, 0, 0)))
        masses = np.array((10, 0))
        n_grid = 5
        L = 15.
        # step = 3
        dens_calc_333 = 10/27
        dens_calc_334 = 10/216*4
        dens_calc_444 = 10/216
        dens_CIC = cic(points, masses, n_grid, L)
        assert dens_CIC[3][3][3] - dens_calc_333 < 1e-6
        assert dens_CIC[3][3][4] - dens_calc_334 < 1e-6
        assert dens_CIC[4][4][4] - dens_calc_444 < 1e-6
"""
import numpy as np
from myCIC import cic
points = np.array(((0, 0, 0), (7.5, 7.5, 7.5), (6, 2, 3)))
masses = np.array((6, 2, 3))
dens_calc = ((5, ))
n_grid = 3
L = 15.
"""