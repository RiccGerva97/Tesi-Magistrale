#!/home/fuffolo97/anaconda3/envs/nbodykit-envB/bin/python

import nbodykit
from nbodykit.lab import *
from nbodykit import style, setup_logging

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
from run_nbk_funcs import cosmo_parser, PacMan, Hartlap, error_message

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
BoxDim = 1000.
line_of_sight = [0, 0, 1]

snapnum = 2

z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]
strt = time.time()
H_0 = 100 * COSMOPAR["fiducial"][2]

root = "/media/fuffolo97/HDD1/UNI/Tesi/halos/"
folders_cosmo = os.listdir(root)


# ===================== EVALUATE POWER SPECTRUM ============================================================

number_coeff_pk = 0

# define dtype for nbk-catalogue
dtype_cust = [("Position", (np.float32, 3)), ("RSDPosition", (np.float32, 3)), ("Velocity", (np.float32, 3)), ("Mass", np.float32)]

print("Beginning the Power Spectrum data evaluation...")

# write files with `picke` for all cosmology in both spaces
for FC in tqdm(range(len(folders_cosmo))):

    # define a cosmology obj for current cosmology folder
    cosmology = cosmology.Cosmology(h = COSMOPAR[folders_cosmo[FC]][2],
                                    sigma8 = COSMOPAR[folders_cosmo[FC]][4],
                                    Omega0_cdm = COSMOPAR[folders_cosmo[FC]][0],
                                    n_s = COSMOPAR[folders_cosmo[FC]][3]
                                    )
    
    root_in = root + folders_cosmo[FC] + '/'
    realizations = os.listdir(root_in)

    # check if the file containing Power Spectrum of the current cosmology already exist
    # create both files for normal and r.d. spaces
    if os.path.exists('./Pk-files/' + folders_cosmo[FC] + '_Pk_nbk.pk'):     os.remove('./Pk-files/' + folders_cosmo[FC] + '_Pk_nbk.pk')
    if os.path.exists('./Pk-files/' + folders_cosmo[FC] + '_Pk_rsd_nbk.pk'): os.remove('./Pk-files/' + folders_cosmo[FC] + '_Pk_rsd_nbk.pk')

    # loop over realizations of a cosmology
    for i in tqdm(range(len(realizations))):
        if folders_cosmo[FC] == "fiducial" and i == 0: continue     # bug for folder '0', must re-download

        snapdir = root_in + realizations[i]

        # reading datas
        datas = FoF_catalog(snapdir, snapnum, read_IDs=False)

        pos_h = (datas.GroupPos  / 1e3 ).astype(np.float32)                   # positions in Mpc/h
        mass  = (datas.GroupMass * 1e10).astype(np.float32)                   # masses in M_sun/
        vel   = (datas.GroupVel  * (1.0+redshift)).astype(np.float32)         # Halo peculiar velocities in km/s

        pos_rsd = []
        for i in range(len(vel)):
            pos_rsd.append(PacMan(pos_h[i] + (1+redshift) * np.array( ([0, 0, vel[i][2]/H_0]) ) ))
        pos_rsd = np.array(pos_rsd, dtype=np.float32)                         # positions in RSD in Mpc/h

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
        mesh_rsd = binCat.to_mesh(resampler='cic', Nmesh=256, compensated=True,
                                  position='RSDPosition', weight="Mass",
                                  BoxSize=BoxDim
                                  )
        
        
        # evaluate FFTPower
        r     = FFTPower(mesh,     mode='1d', dk=0.005, kmin=0.01)
        r_rsd = FFTPower(mesh_rsd, mode='1d', dk=0.005, kmin=0.01)
        
        # get actual Power Spectrum datas
        Pk = r.power
        Pk_rsd = r_rsd.power

        number_coeff_pk = len(Pk["power"].real)

        # store Pk datas in a single file
        with open('./Pk-files/' + folders_cosmo[FC] + '_Pk_nbk.pk', 'ab') as file:
            pickle.dump(Pk, file)
        with open('./Pk-files/' + folders_cosmo[FC] + '_Pk_rsd_nbk.pk', 'ab') as file_rsd:
            pickle.dump(Pk_rsd, file_rsd)

with open("./run_nbk_aaa_usefulInfo.txt", "ab") as ff:
    pickle.dump("Number of Pk coefficients: " + str(number_coeff_pk), ff)

# now i have all the power spectrum info for all realizations for allcosmologies
# I need to take the mean value for all cosmologies and use them to calculate the derivates
# In addition, I have to calculate the covariance matrix for the fiducial cosmology
# It could be useful to create the correlation matrix for fiducial, maybe to compare with the wst one

print("All the Power Spectrum data have been evaluated,\nnow begins the mean value calculus")


#====================== MEAN VALUE =========================================================================

# calculate the mean value for all cosmologies
files_to_proecss = os.listdir('./Pk-files/')

every_mean     = np.zeros((len(cosmological_pars), number_coeff_pk))
every_mean_rsd = np.zeros((len(cosmological_pars), number_coeff_pk))

for FC in tqdm(range(len(files_to_proecss))):
    every_pk = []

    cosmo = cosmo_parser(files_to_proecss[FC])
    assert cosmo in files_to_proecss[FC]
    index = order_folders[cosmo]

    # reading data from files
    with open('./Pk-files/'+files_to_proecss[FC], "rb") as file:
        while True:
            try:
                every_pk.append(pickle.load(file))
            except EOFError:
                break

    # create array with realPower Spectrum
    real_power = []
    for i in range(len(every_pk)):
        real_power.append(every_pk[i]["power"].real  - every_pk[i].attrs['shotnoise'] )

    # assegnate mean value to general array
    if "rsd" not in files_to_proecss[FC]: every_mean[index] = np.mean(real_power, axis=0)
    elif "rsd" in files_to_proecss[FC]:   every_mean_rsd[index] = np.mean(real_power, axis=0)
    else:
        error_message()
        break

print("All the Power Spectrum mean value have been evaluated,\nnow begins the derivates calculus")

#====================== DERIVATES ==========================================================================
# now calculate the derivates
deriavates_pk     = np.zeros((len(cosmological_pars), number_coeff_pk))
deriavates_rsd_pk = np.zeros((len(cosmological_pars), number_coeff_pk))

for i in cosmological_pars:
    if "Mnu" not in i and "Ob" not in i:
        ind = order_dimension[i]
        deriavates_pk[ind]=(every_mean[order_folders[i+"_p"]]-every_mean[order_folders[i+"_m"]])\
                    /  (2 * VarCosmoPar['d_'+i] * fiducial_vals[i] )
        deriavates_rsd_pk[ind]=(every_mean_rsd[order_folders[i+"_p"]]-every_mean_rsd[order_folders[i+"_m"]])\
                    /  (2 * VarCosmoPar['d_'+i] * fiducial_vals[i] )
        #assert derivates_multi_N_pk[order_dimension[i]].all() > 1e-3, f"Derivates of {i} is null"

    elif "Mnu" in i:
        deriavates_pk[order_dimension['Mnu']]     = (deriavates_pk[order_folders["Mnu_p"]]     - every_mean[order_folders["Zeldovich"]])     / (0.1)
        deriavates_rsd_pk[order_dimension['Mnu']] = (deriavates_rsd_pk[order_folders["Mnu_p"]] - every_mean_rsd[order_folders["Zeldovich"]]) / (0.1)
        #assert derivates_multi_N_pk[order_dimension['Mnu']].all() > 1e-3, "Derivates of neutrino mass is null"

    elif "Ob" in i:
        deriavates_pk[order_dimension['Ob']] = \
            (deriavates_pk[order_folders[i+"2_p"]]-deriavates_pk[order_folders[i+"2_m"]]) \
              / (2 * VarCosmoPar['d_'+i+"2"] * fiducial_vals[i] )
        deriavates_rsd_pk[order_dimension['Ob']] = \
            (deriavates_rsd_pk[order_folders[i+"2_p"]]-deriavates_rsd_pk[order_folders[i+"2_m"]]) \
              / (2 * VarCosmoPar['d_'+i+"2"] * fiducial_vals[i] )
        #assert derivates_multi_N_pk[order_dimension['Ob']].all() > 1e-3, "Derivates of Omaga barion is null"


#====================== FISHER MATRIX ======================================================================

nfile_fiducial, nfile_fiducial_rsd = "a", "a"

for i in range(len(files_to_proecss)):
    fn = files_to_proecss[i]
    if "fiducial" in fn and "rsd" not in fn: nfile_fiducial = fn
    if "fiducial" in fn and "rsd"     in fn: nfile_fiducial_rsd = fn

assert type(nfile_fiducial) == type(nfile_fiducial_rsd) == str

fiducial_pk = []
fiducial_rsd_pk = []

with open("./Pk-files/"+nfile_fiducial, "rb") as f:
    while True:
        try:
            fiducial_pk.append(pickle.load(f))
        except EOFError:
            break

with open("./Pk-files/"+nfile_fiducial_rsd, "rb") as f:
    while True:
        try:
            fiducial_rsd_pk.append(pickle.load(f))
        except EOFError:
            break

# create transposed array of Pk coefficients
fiducial_pk = np.array(fiducial_pk).transpose()
fiducial_rsd_pk = np.array(fiducial_rsd_pk).transpose()

# correlation matrix
corr = np.corrcoef(fiducial_pk)
corr_rsd = np.corrcoef(fiducial_rsd_pk)

# covariance matrix
cov = np.cov(fiducial_pk)
cov_rsd = np.cov(fiducial_rsd_pk)

# inverting with Hartlap factor
Hart = Hartlap(cov, 1000)
Hart_rsd = Hartlap(cov_rsd, 1000)

# initialize empty Fisher matrix
Fish, Fish_rsd  = np.zeros((7,7)), np.zeros((7,7))

# create Fisher matrix
for a in range(7):
    for b in range(7):
        Fish[a, b]  = np.sum(deriavates_pk[a]  * (Hart  * deriavates_pk[b]))
        Fish_rsd[a, b]  = np.sum(deriavates_rsd_pk[a]  * (Hart_rsd  * deriavates_rsd_pk[b]))

# GETTING CONATRAINS:
# create inverse of Fisher matrix
inverse = np.linalg.inv(Fish)
inverse_rsd = np.linalg.inv(Fish_rsd)

# initialize empty array containing diagonal elements
diagonal, diagonal_rsd = [], []

# inizialize empty matrix containing all correletions
constrains, constrains_rsd = np.zeros((7,7)), np.zeros((7,7))

# `for loop`: assegnate diaconal elements
for i in range(len(inverse)):
    diagonal.append(np.abs(inverse[i, i])**0.5)
    diagonal_rsd.append(np.abs(inverse_rsd[i, i])**0.5)
    # internal `for loop`: assegnate all the correlations
    for j in range(7):
        constrains[i, j] += np.abs(inverse[i, j])**0.5
        constrains_rsd[i, j] += np.abs(inverse_rsd[i, j])**0.5
        # assert constrains_N_wst[i, j] >= 0

# after checking symmetric elements are almost equal, set them as equal
# this is needed because exact symm. matrix is needed
for i in range(7):
    for j in range(7):
        assert (np.abs(constrains[i, j] - constrains[j, i]) < 1e-5)
        assert (np.abs(constrains_rsd[i, j] - constrains_rsd[j, i]) < 1e-5)
        constrains[i, j] = np.abs(constrains[j, i])
        constrains_rsd[i, j] = constrains_rsd[j, i]

# create correlation graphs, maybe useful to confront with wst
sns.heatmap(corr.transpose())
plt.gca().invert_yaxis()
plt.savefig('correlation_matrix_pk.pdf', format='pdf')

sns.heatmap(corr_rsd.transpose())
plt.gca().invert_yaxis()
plt.savefig('correlation_matrix_rsd_pk.pdf', format='pdf')

# save constrains in a file
with open("./ZZ_results/constrains_pk.res", "ab") as f:
    pickle.dump(constrains, f)
with open("./ZZ_results/constrains_rsd_pk.res", "ab") as f:
    pickle.dump(constrains_rsd, f)