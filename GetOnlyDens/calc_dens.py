import numpy as np
import os, sys
import pickle
from readfof import FoF_catalog
from MAS_library import MA

root = "/media/fuffolo97/HDD1/UNI/Tesi/halos/"

def density_eval(cosmology, i, snapdir, snapnum=2, N_hgrid=256, hlength=1000):
    Shape = (N_hgrid, N_hgrid, N_hgrid)
    datas = FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = (datas.GroupPos/1e3).astype(np.float32)         # positions in Mpc/h
    mass = (datas.GroupMass * 1e10).astype(np.float32)      # masses in M_sun/h
    dens = np.zeros(Shape, dtype=np.float32)
    MA(pos_h, dens, hlength, 'CIC', W = mass)
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0
    print(np.shape(dens), "\n", type(dens), "\n", sys.getsizeof(dens) * 350 * 17 / 1e9,"\n", dens)
    exit()
    with open('/media/fuffolo97/HDD1/UNI/Tesi/densities/'+cosmology+"/"+str(i), 'ab') as file:
        pickle.dump(dens, file)

def iteration_in_cosmology(cosmology):
    in_realizations = os.listdir(root+cosmology)
    for i in range(len(in_realizations)):
        density_eval(cosmology, i, snapdir=root+cosmology+"/"+str(i))
        assert True

cosmo = os.listdir(root)
for i in cosmo:
    iteration_in_cosmology(i)