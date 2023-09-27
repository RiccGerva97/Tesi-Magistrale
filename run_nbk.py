from nbodykit.lab import *
from nbodykit import style, setup_logging

from tqdm import tqdm
import numpy as np
import MAS_library as MASL
import Pk_library as PKL
import matplotlib.pyplot as plt
plt.style.use(style.notebook)

import sys, pickle, time, os

# nbodykit tool to read custom (non-standard) catalogue file type
from nbodykit.io.base import FileType
# nbodykit tool to creae custom subclass od CatalogSource
from nbodykit.source.catalog.file import FileCatalogFactory
# nbodykit cosmology parameters initialization
from nbodykit.lab import cosmology

from readfof import FoF_catalog
from torch import flatten, from_numpy

#---------------------- DICTIONARIES -----------------------------------------------------------------------
COSMOPAR = {
#                   | Om   | Ob   |   h   |  n_s  | s_8 | Mnu | w |

    'fiducial' :    [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    'zeldovich':    [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    
    'Mnu_p' :       [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0.1, -1],
    'Mnu_pp' :      [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0.2, -1],
    'Mnu_ppp' :     [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0.4, -1],
    
    'h_m' :         [0.3175, 0.049, 0.6511, 0.9624, 0.834, 0, -1],
    'h_p' :         [0.3175, 0.049, 0.6911, 0.9624, 0.834, 0, -1],
    
    'ns_m' :        [0.3175, 0.049, 0.6711, 0.9424, 0.834, 0, -1],
    'ns_p' :        [0.3175, 0.049, 0.6711, 0.9824, 0.834, 0, -1],
    
    'Ob_m' :        [0.3175, 0.048, 0.6711, 0.9624, 0.834, 0, -1],
    'Ob_p' :        [0.3175, 0.050, 0.6711, 0.9624, 0.834, 0, -1],
    'Ob2_m' :       [0.3175, 0.047, 0.6711, 0.9624, 0.834, 0, -1],
    'Ob2_p' :       [0.3175, 0.051, 0.6711, 0.9624, 0.834, 0, -1],
    
    'Om_m' :        [0.3075, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    'Om_p' :        [0.3275, 0.049, 0.6711, 0.9624, 0.834, 0, -1],
    
    's8_m' :        [0.3175, 0.049, 0.6711, 0.9624, 0.819, 0, -1],
    's8_p' :        [0.3175, 0.049, 0.6711, 0.9624, 0.849, 0, -1],
    
    'w_m' :         [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -0.95],
    'w_p' :         [0.3175, 0.049, 0.6711, 0.9624, 0.834, 0, -1.05]
}

order_folders = {
    'fiducial'  : 0,
    'h_m'       : 1,
    'h_p'       : 2,
    'Mnu_p'     : 3,
    'Mnu_pp'    : 4,
    'Mnu_ppp'   : 5,
    'ns_m'      : 6,
    'ns_p'      : 7,
    'Ob2_m'     : 8,
    'Ob2_p'     : 9,
    'Om_m'      : 10,
    'Om_p'      : 11,
    's8_m'      : 12,
    's8_p'      : 13,
    'w_m'       : 14,
    'w_p'       : 15,
    'zeldovich' : 16
}

order_dimension = {
    'Om'  : 0,
    'Om ' : 0,
    'Ob'  : 1,
    'Ob ' : 1,
    'Ob2' : 1,
    'h'   : 2,
    'h  ' : 2,
    'ns'  : 3,
    'ns ' : 3,
    's8'  : 4,
    's8 ' : 4,
    'w'   : 5,
    'Mnu' : 6
}

cosmological_pars = {
    'Om'  : 0,
    'Ob'  : 1,
    'h'   : 2,
    'ns'  : 3,
    's8'  : 4,
    'w'   : 5,
    'Mnu' : 6
}

VarCosmoPar = {
    'd_h'  : 0.02, 'd_ns' : 0.02, 'd_Ob' : 0.001, 'd_Ob2': 0.002,
    'd_Om' : 0.01, 'd_s8' : 0.015, 'd_w'  : -0.05
}

fiducial_vals = {
    'Ob'  : 0.3175,
    'Ob2' : 0.3175,
    'Om'  : 0.049,
    'h'   : 0.6711,
    'n_s' : 0.9624,
    'ns'  : 0.9624,
    's_8' : 0.834,
    's8'  : 0.834,
    'Mnu' : 0,
    'w'   : -1
}

#---------------------- FUNCTIONS --------------------------------------------------------------------------
def info_name(name):
    """Obtain realization information from namefile"""
    # assert type(name) == str
    print("TYPE: ", type(name))
    # info = name.split('_')
    info = name.split('_')[-3:]
    print("TYPE: ", info, "\n", type(info))
    info[2] = info[2].replace(".wst", "")
    N_hgrid = info[0]
    N_WSTgrid = info[1]
    n_realiz = info[2].replace(".wst", "")
    
    return [int(N_hgrid), int(N_WSTgrid), int(n_realiz)]

def cosmo_parser(name):
    """Obtain cosmology from .wst file"""
    info = name.split('_')
    if info[0] == "fiducial":
        return info[0]
    elif info[0] == "zeldovich":
        return info[0]
    else:
        return info[0] + "_" + info[1]
    
def PacMan(x, d = np.array((0, 0, 1000)) ):
    """Returns a number x in the interval [0; d]"""
    if 0 <= x[2] <= d[2]:
        return x
    elif x[2] > d[2]:
        return PacMan(x - d)
    elif x[2] < 0:
        return PacMan(x + d)
    

#====================== MAIN CODE ==========================================================================
# basic variables    
N_grid = 256
BoxDim = 1000.
line_of_sight = [0, 0, 1]

snapnum = 2

z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]
strt = time.time()
H_0 = 100 * COSMOPAR["fiducial"][2]

root = "/media/fuffolo97/HDD1/UNI/Tesi/halos/"
folders_cosmo = os.listdir(root)

# define dtype for nbk-catalogue
dtype_cust = [("Position", (np.float32, 3)), ("RSDPosition", (np.float32, 3)), ("Velocity", (np.float32, 3)), ("Mass", np.float32)]

for FC in range(len(folders_cosmo)):

    # define a cosmology obj for current cosmology folder
    cosmology = cosmology.Cosmology(h = COSMOPAR[folders_cosmo[FC]][2],
                                    sigma8 = COSMOPAR[folders_cosmo[FC]][4],
                                    Omega0_cdm = COSMOPAR[folders_cosmo[FC]][0],
                                    n_s = COSMOPAR[folders_cosmo[FC]][3]
                                    )
    
    root_in = root + folders_cosmo[FC] + '/'
    realizations = os.listdir(root_in)

    # check if the file containing Power Spectrum of the current cosmology already exist
    if os.path.exists('./Pk-files/' + folders_cosmo[FC] + '_Pk_nbk.pk'): os.remove('./Pk-files/' + folders_cosmo[FC] + '_Pk_nbk.pk')
    if os.path.exists('./Pk-files/' + folders_cosmo[FC] + '_Pk_rds_nbk.pk'): os.remove('./Pk-files/' + folders_cosmo[FC] + '_Pk_rds_nbk.pk')

    # loop over realizations of a cosmology
    for i in range(len(realizations)):
        snapdir = root_in + realizations[i]

        # reading datas
        datas = FoF_catalog(snapdir, snapnum, read_IDs=False)

        pos_h = (datas.GroupPos / 1e3).astype(np.float32)                    # positions in Mpc/h
        mass  = (datas.GroupMass * 1e10).astype(np.float32)                  # masses in M_sun/
        vel   = (datas.GroupVel * (1.0+redshift)).astype(np.float32)         # Halo peculiar velocities in km/s

        pos_rsd = []
        for i in range(len(vel)):
            pos_rsd.append(PacMan(pos_h[i] + (1+redshift) * np.array( ([0, 0, vel[i][2]/H_0]) ) ))
        pos_rsd = np.array(pos_rsd, dtype=np.float32)                        # positions in RSD in Mpc/h

        # create fale to store data
        if os.path.exists('./data_source.dat'): os.remove('./data_source.dat')

        with open('./data_source.dat', "wb") as ff:
            pos_h.tofile(ff); pos_rsd.tofile(ff); vel.tofile(ff); mass.tofile(ff)
            ff.seek(0)

        # create nbodykit BinaryCatalog
        binCat = BinaryCatalog(ff.name, dtype_cust)

        # create mesh
        mesh = binCat.to_mesh(resampler='cic', Nmesh=256, compensated=True,
                              position='Position', weight="Mass",
                              BoxSize=BoxDim
                              )
        mesh_rds = binCat.to_mesh(resampler='cic', Nmesh=256, compensated=True,
                                  position='RDSPosition', weight="Mass",
                                  BoxSize=BoxDim
                                  )
        
        
        # evaluate FFTPower
        r = FFTPower(mesh, mode='1d', dk=0.005, kmin=0.01)
        r_rds = FFTPower(mesh_rds, mode='1d', dk=0.005, kmin=0.01)
        # get actual Power Spectrum datas
        Pk = r.power
        Pk_rds = r_rds.power

        # store Pk datas in a single file
        with open('./Pk-files/' + folders_cosmo[FC] + '_Pk_nbk.pk', 'ab') as file: pickle.dump(Pk, file)
        with open('./Pk-files/' + folders_cosmo[FC] + '_Pk_rds_nbk.pk', 'ab') as file_rds: pickle.dump(Pk_rds, file_rds)

# now i have all the power spectrum info for all realizations for allcosmologies
# I need to take the mean value for all cosmologies and use them to calculate the derivates
# In addition, I have to calculate the covariance matrix for the fiducial cosmology
# It could be useful to create the correlation matrix for fiducial, maybe to compare with the wst one

# calculate the mean value for all cosmologies
files_to_proecss = os.listdir('./Pk-files/')

every_mean = []
every_mean_rsd = []

for FC in range(len(files_to_proecss)):
    every_pk = []

    with open('./Pk-files/'+files_to_proecss[FC], "rb") as file:
        while True:
            try:
                every_pk.append(pickle.load(file))
            except EOFError:
                break

    real_power = []
    for i in range(len(every_pk)):
        real_power.append(every_pk[i]["power"].real  - every_pk[i].attrs['shotnoise'] )

    if "rsd" not in files_to_proecss[FC]:
        every_mean.append(np.mean(real_power, axis=0))
    elif "rsd" in files_to_proecss[FC]:
        every_mean_rsd.append(np.mean(real_power, axis=0))
    else:
        print("ERROR >.<")
        break 

# now calculate the derivates
deriavates_pk = np.zeros((len(cosmological_pars), len(multi_tot_N_pk[0])))

for i in cosmological_pars:
    if "Mnu" not in i and "Ob" not in i:
        ind = order_dimension[i]
        deriavates_pk[ind]=(every_mean[order_folders[i+"_p"]]-every_mean[order_folders[i+"_m"]])\
                    /  (2 * VarCosmoPar['d_'+i] * fiducial_vals[i] )
        #assert derivates_multi_N_pk[order_dimension[i]].all() > 1e-3, f"Derivates of {i} is null"

    elif "Mnu" in i:
        deriavates_pk[order_dimension['Mnu']] = (deriavates_pk[order_folders["Mnu_p"]] - zeldovich_multi_N_avg) / (0.1)
        #assert derivates_multi_N_pk[order_dimension['Mnu']].all() > 1e-3, "Derivates of neutrino mass is null"

    elif "Ob" in i:
        deriavates_pk[order_dimension['Ob']] = \
            (deriavates_pk[order_folders[i+"2_p"]]-deriavates_pk[order_folders[i+"2_m"]]) \
              / (2 * VarCosmoPar['d_'+i+"2"] * fiducial_vals[i] )
        #assert derivates_multi_N_pk[order_dimension['Ob']].all() > 1e-3, "Derivates of Omaga barion is null"