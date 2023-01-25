import numpy as np
from myCIC import cic

import unittest

# python -m pytest test_CIC.py 

class TestCIC(unittest.TestCase):
    def test_density(self):
        points = np.array(((7.5, 7.5, 7.5), (1.5, 1.5, 1.5), (21.5, 22.5, 23.5)))
        masses = np.array((10, 20, 5))
        n_grid = 10
        L = 30.

        # counting cells 0-1-2-...-9
        # points are in gir dcells: (2, 2, 2), (0, 0, 0) and (7, 7, 7)
        dens_calc_222 = 10/216 * 8              # cell of 1st point
        dens_calc_223 = 10/126 * 4              # cell with a common face with the one of 1st point
        dens_calc_333 = 10/216                  # cell with a single common vertice "
        dens_calc_000 = 20/216 * 8              # cell of 2nd point
        dens_calc_111 = 30/216                  # cell between 1st & 2nd point, both only one vertice
        dens_calc_999 = 20/216                  # dell opposite to 2nd point -> test periodic BC
        dens_calc_777 = 5/216 * 8               # cell of 3rd point
        dens_calc_666 = 5/729 * (0.5*1.5*2.5)   # cell with a single common vertice with the 3rd point
        
        dens_CIC = cic(points, masses, n_grid, L)
        
        assert dens_CIC[2][2][2] - dens_calc_222 < 1e-10
        assert dens_CIC[2][2][3] - dens_calc_223 < 1e-10
        assert dens_CIC[3][3][3] - dens_calc_333 < 1e-10
        assert dens_CIC[0][0][0] - dens_calc_000 < 1e-10
        assert dens_CIC[1][1][1] - dens_calc_111 < 1e-10
        assert dens_CIC[9][9][9] - dens_calc_999 < 1e-10
        assert dens_CIC[7][7][7] - dens_calc_777 < 1e-10
        assert dens_CIC[6][6][6] - dens_calc_666 < 1e-10