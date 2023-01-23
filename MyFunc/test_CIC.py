import numpy as np
from myCIC import cic

import unittest

class TestCIC(unittest.TestCase):
    def test_density(self):
        points = np.array(((7.5, 7.5, 7.5), (1.5, 1.5, 1.5)))
        masses = np.array((10, 20))
        n_grid = 5
        L = 15.

        # counting cells 0-1-2-3-4
        # points are in (2, 2, 2) and (0, 0, 0)
        dens_calc_222 = 10/216 * 8          # cell of 1st point
        dens_calc_223 = 10/126 * 4          # cell with a common face with the one of 1st point
        dens_calc_333 = 10/216              # cell with a single common vertice "
        dens_calc_000 = 20/216 * 8          # cell of 2nd point
        dens_calc_111 = 30/216              # cell between 1st & 2nd point, both only one vertice
        
        dens_CIC = cic(points, masses, n_grid, L)
        
        assert dens_CIC[2][2][2] - dens_calc_222 < 1e-10
        assert dens_CIC[2][2][3] - dens_calc_223 < 1e-10
        assert dens_CIC[3][3][3] - dens_calc_333 < 1e-10
        assert dens_CIC[0][0][0] - dens_calc_000 < 1e-10
        assert dens_CIC[1][1][1] - dens_calc_111 < 1e-10