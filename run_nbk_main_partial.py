# this script executes only a folder

import nbodykit
from nbodykit.lab import *
from nbodykit import style, setup_logging
import redshift_space_library
# import corner
from tqdm import tqdm
import numpy as np
import seaborn as sns
import MAS_library as MASL
import Pk_library as PKL
import matplotlib.pyplot as plt

import sys, pickle, time, os
# sys.path.insert(1, './')
from run_nbk_dict import COSMOPAR, order_dimension, order_folders, cosmological_pars, \
                         VarCosmoPar, fiducial_vals
from run_nbk_funcs import cosmo_parser, PacMan, Hartlap, HubblePar, \
                          covariation_matrix, error_message

# nbodykit tool to read custom (non-standard) catalogue file type
from nbodykit.io.base import FileType
# nbodykit tool to creae custom subclass od CatalogSource
from nbodykit.source.catalog.file import FileCatalogFactory
# nbodykit cosmology parameters initialization
from nbodykit.lab import cosmology

from readfof import FoF_catalog
from torch import flatten, from_numpy

# basic variables    
N_grid = 256
N_mesh = 512
BoxDim = 1000.
line_of_sight = [0, 0, 1]

snapnum = 2

z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]
strt = time.time()
H_0 = 100 * COSMOPAR["fiducial"][2]

root_in = "/media/fuffolo97/HDD1/UNI/Tesi/halos/fiducial/"

# ===================== EVALUATE POWER SPECTRUM ============================================================

number_coeff_pk = 0

# define dtype for nbk-catalogue
dtype_cust = [("Position", (np.float32, 3)), ("RSDPosition", (np.float32, 3)), ("Velocity", (np.float32, 3)), ("Mass", np.float32)]

error_message("Beginning the Power Spectrum data evaluation...")

realizations = os.listdir(root_in)

for i in tqdm(range(len(realizations))):
    snapdir = root_in + realizations[i]

    # reading datas
    datas = FoF_catalog(snapdir, snapnum, read_IDs=False)

    pos_h = (datas.GroupPos  / 1e3 ).astype(np.float32)                   # positions in Mpc/h
    mass  = (datas.GroupMass * 1e10).astype(np.float32)                   # masses in M_sun/
    vel   = (datas.GroupVel  * (1.0+redshift)).astype(np.float32)         # Halo peculiar velocities in km/s
    
    H_cosmo = HubblePar(z = redshift, O_m = fiducial_vals["Om"], H_0 = fiducial_vals["h"],\
                        w = fiducial_vals["w"])

    pos_rsd = []
    for i in range(len(vel)):
        # pos_rsd.append(PacMan(pos_h[i] + (1+redshift) * np.array( ([0, 0, vel[i][2]/H_0]) ) ))
        pos_rsd.append(PacMan(pos_h[i] + (1+redshift) * np.array( ([0, 0, vel[i][2]/ H_cosmo ]) ) ))
    pos_rsd = np.array(pos_rsd, dtype=np.float32)                         # positions in RSD in Mpc/h

    # create fale to store data
    if os.path.exists('./data_source.dat'): os.remove('./data_source.dat')

    with open('./data_source.dat', "wb") as ff:
        pos_h.tofile(ff); pos_rsd.tofile(ff); vel.tofile(ff); mass.tofile(ff)
        ff.seek(0)

    # create nbodykit BinaryCatalog
    binCat = BinaryCatalog(ff.name, dtype_cust)

    # create mesh
    mesh = binCat.to_mesh(resampler='cic', Nmesh=N_mesh, compensated=True,
                            position='Position', weight="Mass",
                            #compensated = True, # antialiasing
                            BoxSize=BoxDim
                            )
    mesh_rsd = binCat.to_mesh(resampler='cic', Nmesh=N_mesh, compensated=True,
                                position='RSDPosition', weight="Mass",
                                #compensated = True, # antialiasing
                                BoxSize=BoxDim
                                )
    
    # evaluate FFTPower
    r = FFTPower(mesh, mode='1d', dk=0.005, kmin=0.01)
    r_rsd = FFTPower(mesh_rsd, mode='1d', dk=0.005, kmin=0.01)
    
    # get actual Power Spectrum datas
    Pk = r.power
    Pk_rsd = r_rsd.power

    # store Pk datas in a single file
    with open('./Pk-files/fiducial_Pk_nbk.pk', 'ab') as file:
        pickle.dump(Pk, file)
    with open('./Pk-files/fiducial_Pk_rsd_nbk.pk', 'ab') as file_rsd:
        pickle.dump(Pk_rsd, file_rsd)

error_message("END!")