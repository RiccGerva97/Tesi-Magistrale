import numpy as np

def cic(pos: np.ndarray, mass: np.ndarray, N_grid: int, length=1000):
    """A simple Cloud in a Cell algorithm, written in order to study halo catalogue from Quijote simulations.
    
    Arguments:
    - `pos` : a numpy.ndarray containing halos' positions;
    - `mass` : an array containing halos' masses;
    - `N_grid` : numbers of cells per lenght; grid must be cubic;
    - `length` : total length of the simulation; default value (based on Quijote simul) 1000 Mpc/h.
    
    Returns:
    - density matrix, type: numpy.float32
    """

    N_points = len(pos)
    step = length/N_grid
    density = np.float32(np.zeros((N_grid, N_grid, N_grid)))
    
    # matrix that contains grid coordinates per particle
    cells = np.array(np.fix(pos/step), dtype=np.int16)
    
    # contains arrays of distance between the point and the node that indexes the cell
    dists = np.float32(pos - cells*step)
    
    # vectors for calculate all the cube vertices weights
    vecs = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)), dtype=np.int8)
    
    # for loops over all points
    for i in range(N_points):
        miafunzione(mass[i], N_grid, step, density, cells[i], dists[i], vecs)

    return np.float32(pow(step, -6) * density)

def miafunzione(m: float, N_grid: int, step: float, density, CELL, DIST, vecs):
    """A function that takes halo parameters and its distribution information and calculates its contribution 
    to every veritces of its cell; than it assegnates those values to the communicating cells.
    n.b.: modifies `density`.
    """
    
    cube = np.zeros((2, 2, 2))
    for v in vecs:
        cube[v[0]][v[1]][v[2]] += m*np.abs(np.prod(((1-v)*step-DIST)))

    for a in [0,1]:                               # \
        for b in [0,1]:                           # |-> indeces for cube[]
            for c in [0,1]:                       # /
                for l in np.where( CELL + [a, b, c] == N_grid )[0]:     # control for periodic b.c.
                    CELL[l]=-1
                
                cubo = cube[a][b][c]
                cell0 = CELL[0]
                cell1 = CELL[1]
                cell2 = CELL[2]
                
                density[cell0+a][cell1+b][cell2+c-1] += cubo
                density[cell0+a][cell1+b][cell2+c] += cubo
                density[cell0+a][cell1+b-1][cell2+c-1] += cubo
                density[cell0+a][cell1+b-1][cell2+c] += cubo
                density[cell0+a-1][cell1+b][cell2+c-1] += cubo
                density[cell0+a-1][cell1+b][cell2+c] += cubo
                density[cell0+a-1][cell1+b-1][cell2+c-1] += cubo
                density[cell0+a-1][cell1+b-1][cell2+c] += cubo
