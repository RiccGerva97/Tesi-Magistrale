import numpy as np
import time

def cic(pos: np.ndarray, mass: np.ndarray, N_grid: int, length=1000):
    """
    A simple Cloud in a Cell algorithm, written in rder to study halo
    catalogue from Quijote simulations.
    Arguments:
    - pos: a numpy.ndarray containing halos' positions;
    - mass: an array containing halos' masses;
    - N_grid: numbers of cells per lenght; grid must be cubic;
    - length: total length of the simulation; default value (based on Quijote simul) 1000 Mpc/h.
    
    Returns a 'N_grid^3' density matrix.
    """

    step = length/N_grid
    density = np.float32(np.zeros((N_grid, N_grid, N_grid)))
    
    # matrix that contains grid coordinates per particle
    cells = np.array(np.fix(pos/step), dtype=np.int8)
    
    # contains arrays of distance between the point and the node that indexes the cell
    dists = np.float32(pos - cells*step)
    
    # vectors for calculate all the cube vertices weights
    vecs = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)), dtype=np.int8)
    
    # t = time.time()
    
    for i in range(len(pos)):
        # m = mass[i]
        # d = dists[i]
        cube = np.zeros((2, 2, 2))

        # for loop: calculates the weights of every vertices of the point cell
        for v in vecs:
            # cube[v[0]][v[1]][v[2]] += m*np.abs(np.prod(((1-v)*step-d)))
            cube[v[0]][v[1]][v[2]] += mass[i]*np.abs(np.prod(((1-v)*step-dists[i])))

        # for loops: assigns to every cell that contains the same vertice its value
        for a in range(2):                              # \
            for b in range(2):                          # |-> indeces for cube[]
                for c in range(2):                      # /
                    for x in [-1, 0]:                   # \
                        for y in [-1, 0]:               # |-> indeces for cells[]
                            for z in [-1, 0]:           # /
                                if np.any(cells[i]+(a, b, c) == N_grid):
                                    for l in np.where(cells[i]+(a, b, c)==N_grid):
                                        cells[i][l]=-1
                                
                                density[cells[i][0]+x+a][cells[i][1]+y+b][cells[i][2]+z+c] += cube[a][b][c]
        # if i==0:
        #     print("One cycle time: ", time.time()-t)

    return np.float32(pow(step, -6) * density)