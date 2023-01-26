import numpy as np
# from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process

# import time

def cic_multiP(pos: np.ndarray, mass: np.ndarray, N_grid: int, length=1000):
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
    
    cells = np.array(np.fix(pos/step), dtype=np.int16)      # matrix that contains grid coordinates per particle
    
    dists = np.float32(pos - cells*step)                    # contains arrays of distance between the point and
                                                            # the node that indexes the cell
    
    # vectors for calculate all the cube vertices weights
    vecs = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), \
            (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)), dtype=np.int8)

    # pool = ThreadPool(4)

    results = None
    for i in range(N_points):
        results = Process(target = miafunzione, args = (mass, N_grid, step, density, cells, dists, vecs, i))
        results.start()

    print(np.shape(results))
    DD = np.sum(results)
    results.close()
    return np.float32(pow(step, -6) * DD)


def miafunzione(mass, N_grid, step, density, cells, dists, vecs, i):
    cube = np.zeros((2, 2, 2))
    # print("mass: ", mass, "\nmass[i]: ", mass [i], " \nmass[i][0]: ", mass[i][0], "\n")
    for v in vecs:
        cube[v[0]][v[1]][v[2]] += mass[i]*np.abs(np.prod(((1-v)*step-dists[i])))

    CELL = cells[i]

    for a in range(2):                              # \
        for b in range(2):                          # |-> indeces for cube[]
            for c in range(2):                      # /
                for x in [-1, 0]:                   # \
                    for y in [-1, 0]:               # |-> indeces for cells[]
                        for z in [-1, 0]:           # /
                            for l in np.where( CELL + [a, b, c] == N_grid )[0]:
                                CELL[l]=-1
                            #print("density: ", np.shape(density), "\n       ", np.shape(density[c[0]+x+a][c[1]+y+b][c[2]+z+c]),\
                            #        "cube: ",cube, "\n      ", cube[a][b][c])
                            density[CELL[0]+x+a][CELL[1]+y+b][CELL[2]+z+c] += cube[a][b][c]

    return density