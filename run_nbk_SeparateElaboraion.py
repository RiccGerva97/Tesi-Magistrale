#!/home/fuffolo97/anaconda3/envs/nbodykit-envB/bin/python

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

number_coeff_pk = 320

# calculate the mean value for all cosmologies
files_to_proecss = os.listdir('./Pk-files/')
number_of_files = int(len(files_to_proecss) / 2)
every_mean     = np.zeros((number_of_files, number_coeff_pk))
every_mean_rsd = np.zeros((number_of_files, number_coeff_pk))

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
    if "rsd" not in files_to_proecss[FC]: every_mean[index] += np.mean(real_power, axis=0)
    elif "rsd" in files_to_proecss[FC]:   every_mean_rsd[index] += np.mean(real_power, axis=0)
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
        deriavates_pk[order_dimension['Mnu']]     \
            = (every_mean[order_folders["Mnu_p"]]     - every_mean[order_folders["zeldovich"]])     / (0.1)
        deriavates_rsd_pk[order_dimension['Mnu']] = (every_mean_rsd[order_folders["Mnu_p"]] - every_mean_rsd[order_folders["zeldovich"]]) / (0.1)
        #assert derivates_multi_N_pk[order_dimension['Mnu']].all() > 1e-3, "Derivates of neutrino mass is null"

    elif "Ob" in i:
        deriavates_pk[order_dimension['Ob']] = \
            (every_mean[order_folders[i+"2_p"]]-every_mean[order_folders[i+"2_m"]]) \
              / (2 * VarCosmoPar['d_'+i+"2"] * fiducial_vals[i] )
        deriavates_rsd_pk[order_dimension['Ob']] = \
            (every_mean_rsd[order_folders[i+"2_p"]]-every_mean_rsd[order_folders[i+"2_m"]]) \
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

fiducial_pk_pk, fiducial_rsd_pk_pk = [], []
for i in range(len(fiducial_pk)):
    fiducial_pk_pk.append(fiducial_pk[i]["power"].real  - fiducial_pk[i].attrs['shotnoise'] )
    fiducial_rsd_pk_pk.append(fiducial_rsd_pk[i]["power"].real  - fiducial_rsd_pk[i].attrs['shotnoise'] )

# create transposed array of Pk coefficients
fiducial_pk = np.array(fiducial_pk_pk).transpose()
fiducial_rsd_pk = np.array(fiducial_rsd_pk_pk).transpose()

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
        assert (np.abs((constrains[i, j] - constrains[j, i])/constrains[i, j]) < 1e-5)
        assert (np.abs((constrains[i, j] - constrains[j, i])/constrains[j, i]) < 1e-5)
        assert (np.abs(constrains_rsd[i, j] - constrains_rsd[j, i]) < 1e-5)
        assert (np.abs((constrains_rsd[i, j] - constrains_rsd[j, i])/constrains_rsd[i, j]) < 1e-5)
        assert (np.abs((constrains_rsd[i, j] - constrains_rsd[j, i])/constrains_rsd[j, i]) < 1e-5)
        # constrains[i, j] = np.abs(constrains[j, i])
        # constrains_rsd[i, j] = constrains_rsd[j, i]
        if i > j:
            constrains[i, j] = constrains[j, i]
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