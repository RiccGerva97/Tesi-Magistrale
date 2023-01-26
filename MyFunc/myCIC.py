import numpy as np
from multiprocessing import Process
from multiprocessing.dummy import Pool as ThreadPool
import itertools
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# import time

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
    # t = time.time()
    N_points = len(pos)
    step = length/N_grid
    density = np.float32(np.zeros((N_grid, N_grid, N_grid)))
    
    # matrix that contains grid coordinates per particle
    cells = np.array(np.fix(pos/step), dtype=np.int16)
    
    # contains arrays of distance between the point and the node that indexes the cell
    dists = np.float32(pos - cells*step)
    
    # vectors for calculate all the cube vertices weights
    vecs = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)), dtype=np.int8)
    
    # T1 = time.time() - t
    # T2 = time.time()
    
    for i in range(N_points):
        miafunzione1(mass[i], N_grid, step, density, cells[i], dists[i], vecs)

    # print("Before for loops: ", T1, "\nFor loops: ", time.time()-T2)
    
    return np.float32(pow(step, -6) * density)

#------------------------------------------------------------------------------------------------------------------
#   cic function using multiprocess.Process method
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

#    results = []
#    for i in range(4):
#        start = int(i*N_points/4)
#        end = int((i+1)*N_points/4)
#        p = Process(target = lambda i: miafunzione(mass, N_grid, step, density, cells, dists, vecs, i), args=(start, end))
    # for i in range(N_points):
    #    results = Process(target = miafunzione, args = (mass, N_grid, step, density, cells, dists, vecs, i))
#        results.append(p)
#        p.start()
    
#    for p in results:
#        p.join()

    procs = []
    p = Process(target=miafunzione)
    procs.append(p)
    p.start()

    for i in range(N_points):
        p = Process(target=miafunzione1(mass[i], N_grid, step, density, cells[i], dists[i], vecs), args=(i,))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()
    p.close()
    #print(p, "\n", np.shape(p), "  ", type(p))
    #print(results, "\n", np.shape(results), "  ", type(results))
    DD = np.sum(results)
    return np.float32(pow(step, -6) * DD)

#------------------------------------------------------------------------------------------------------------------
#   cic function using multiprocess.thread.Pool method
#------------------------------------------------------------------------------------------------------------------
def cic_multiT(pos: np.ndarray, mass: np.ndarray, N_grid: int, length=1000):
    """A simple Cloud in a Cell algorithm, written in order to study halo catalogue from Quijote simulations.
    
    Arguments:
    - `pos` : a numpy.ndarray containing halos' positions;
    - `mass` : an array containing halos' masses;
    - `N_grid` : numbers of cells per lenght; grid must be cubic;
    - `length` : total length of the simulation; default value (based on Quijote simul) 1000 Mpc/h.
    
    Returns:
    - density matrix, type: numpy.float32
    """

    import time
    start = time.time()

    N_points = len(pos)
    step = length/N_grid
    density = np.float32(np.zeros((N_grid, N_grid, N_grid)))
    
    cells = np.array(np.fix(pos/step), dtype=np.int16)      # matrix that contains grid coordinates per particle
    dists = np.float32(pos - cells*step)                    # contains arrays of distance between the point and
                                                            # the node that indexes the cell
    
    # vectors for calculate all the cube vertices weights
    vecs = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), \
            (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)), dtype=np.int8)

    pool = ThreadPool(3)

    def innerfunction(range_i):
        start = time.time()
        result = miafunzione_mT(mass, N_grid, step, cells, dists, vecs, range_i)
        print(f"Un thread terminato in {time.time() - start} secondi")
        return result

    results = pool.map(
        # lambda range_of_i: miafunzione_mT(mass, N_grid, step, cells, dists, vecs, range_of_i),
        innerfunction,
        [range(i * N_points // 3, (i+1) * N_points // 3) for i in range(3)]

        # [range(0, N_points//6), 
        # range(N_points//6, N_points//3), range(N_points//3, N_points//2), range(N_points//2, 2*N_points//3),\
        #     range(2*N_points//3, 5*N_points//6), range(5*N_points//6, N_points)]
    )

        # [range(0, N_points//4), range(N_points//4, N_points//2), range(N_points//2, 3*N_points//4), range(3*N_points//4, N_points)]
    #    )
    
    #density = pool.map(miafunzione1(mass, N_grid, step, density, cells, dists, vecs), range(N_points))

    # results = pool.map(lambda i: miafunzione_mT(mass, N_grid, step, density, cells, dists, vecs, i), range(N_points))
    # results = pool.map(lambda i:\
    #                                 miafunzione_mT(mass, N_grid, step, density, cells, dists, vecs, i), \
    #                         range(N_points)\
    #                                                 )
    pool.close()
    pool.join()
    # pool.close()
    #pool.join()
    print("TEMPO COMPLESSIVO: ", (time.time() - start))

 #   threads = []
#    for i in range(4):
#        start = int(i*N_points/4)
#        end = int((i+1)*N_points/4)
#        t = Thread(target=lambda j: miafunzione(mass[i], N_grid, step, density, cells[i], dists[i], vecs, j), args = (start, end))
#        threads.append(t)
#        t.start()
#    for t in threads:
 #        t.join()


    # return np.float32(pow(step, -6) * np.sum(results))

    out = results[0]
    for intermediate_result in results[1:]:
        out += intermediate_result
    return np.float32(pow(step,-6) * out)

    # return results


def miafunzione1(m, N_grid, step, density, CELL, DIST, vecs):
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
                
                # for x in [-1, 0]:                   # \
                #     for y in [-1, 0]:               # |-> indeces for cells[]
                #         for z in [-1, 0]:           # /            
                #             #print("density: ", np.shape(density), "\n       ", np.shape(density[c[0]+x+a][c[1]+y+b][c[2]+z+c]),\
                #             #        "cube: ",cube, "\n      ", cube[a][b][c])
                #             density[cell0+x+a][cell1+y+b][cell2+z+c] += cubo

def miafunzione(mass, N_grid, step, density, cells, dists, vecs, i):
    cube = np.zeros((2, 2, 2))
    for v in vecs:
        cube[v[0]][v[1]][v[2]] += mass[i]*np.abs(np.prod(((1-v)*step-dists[i])))

    CELL = cells[i]

    for a in range(2):                              # \
        for b in range(2):                          # |-> indeces for cube[]
            for c in range(2):                      # /
                for x in [-1, 0]:                   # \
                    for y in [-1, 0]:               # |-> indeces for cells[]
                        for z in [-1, 0]:           # /
                            for l in np.where( CELL + [a, b, c] == N_grid )[0]:     # control for periodic b.c.
                                CELL[l]=-1
                            #print("density: ", np.shape(density), "\n       ", np.shape(density[c[0]+x+a][c[1]+y+b][c[2]+z+c]),\
                            #        "cube: ",cube, "\n      ", cube[a][b][c])
                            density[CELL[0]+x+a][CELL[1]+y+b][CELL[2]+z+c] += cube[a][b][c]

    return density

def miafunzione_mT(mass, N_grid, step, cells, dists, vecs, range_i):
    density = np.float32(np.zeros((N_grid, N_grid, N_grid)))

    for i in range_i:
        cube = np.zeros((2, 2, 2))
        # print("mass: ", mass, "\nmass[i]: ", mass[i], " \nmass[i][0]: ", mass[i][0], "\n")
        # print("cells: ", cells, "\ncells[i]: ", cells[i], " \ncells[i][0]: ", cells[i][0], "\n\n")
        for v in vecs:
            cube[v[0]][v[1]][v[2]] += mass[i]*np.abs(np.prod(((1-v)*step-dists[i])))

        CELL = cells[i]

        for a in range(2):                              # \
            for b in range(2):                          # |-> indeces for cube[]
                for c in range(2):                      # /
                    for x in [-1, 0]:                   # \
                        for y in [-1, 0]:               # |-> indeces for cells[]
                            for z in [-1, 0]:           # /
                                for l in np.where( CELL + [a, b, c] == N_grid )[0]:     # control for periodic b.c.
                                    CELL[l]=-1
                                #print("density: ", np.shape(density), "\n       ", np.shape(density[c[0]+x+a][c[1]+y+b][c[2]+z+c]),\
                                #        "cube: ",cube, "\n      ", cube[a][b][c])
                                density[CELL[0]+x+a][CELL[1]+y+b][CELL[2]+z+c] += cube[a][b][c]

    return density