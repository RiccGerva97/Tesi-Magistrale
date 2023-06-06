import numpy as np
import os
import pickle

import sys
sys.path.insert(1, './MyFunc')
from MyFunc.myDict import order_folders, order_dimension, COSMOPAR, VarCosmoPar, fiducial_vals, cosmological_pars
from MyFunc.name_parser import cosmo_parser
from MyFunc.Fisher import correlation_matrix, Hartlap

# def FISHER_EVAL(root = "../WST-files", n_realiz = 350):
n_realiz = 1000
root = "/home/riccardo/WST-files/"
cosmologies = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
            'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', 'Om_m', 'Om_p', \
            's8_m', 's8_p', 'w_m', 'w_p', 'zeldovich']

fiducial_coeffs = []
zeldovich_coeffs = []

coeffs_tot = np.zeros((len(cosmologies), 75))
files_to_read = os.listdir(root)

for i in range(len(files_to_read)):
    coeffs_cosm = []
    file_reading = files_to_read[i]

    cosmo = cosmo_parser(file_reading)
    assert cosmo in file_reading
    index = order_folders[cosmo]
    
    if "fiducial" not in file_reading and "zeldovich" not in file_reading:
        with open(root + "/" + file_reading, 'rb') as Ff:
            while True:
                try:
                    coeffs_cosm.append(pickle.load(Ff))
                except EOFError:
                    break
    elif "fiducial" in file_reading:
        with open(root + "/" + file_reading, 'rb') as Ff:
            while True:
                try:
                    fiducial_coeffs.append(pickle.load(Ff))
                except EOFError:
                    break
    elif "zeldovich" in file_reading:
        with open(root + "/" + file_reading, 'rb') as Ff:
            while True:
                try:
                    zeldovich_coeffs.append(pickle.load(Ff))
                except EOFError:
                    break
    else:
        assert False, "\n   ERROR in reading WST files, cosmology can't be propely interpreted.\n"

    coeffs_tot[index] = np.average(coeffs_cosm, axis=0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FISHER MATRIX

derivates = np.zeros((len(cosmological_pars), len(coeffs_tot[0])))
for i in cosmological_pars:
    if "Mnu" not in i and "Ob" not in i:
        ind = order_dimension[i]
        derivates[ind]=(coeffs_tot[order_folders[i+"_p"]]-coeffs_tot[order_folders[i+"_m"]])\
            / (2 * VarCosmoPar['d_'+i] * fiducial_vals[i] )
        assert derivates[order_dimension[i]].all() != 0, f"Derivates of {i} is null"
    elif "Mun" in i:
        derivates[order_dimension['Mnu']] = \
            (coeffs_tot[order_folders['Mnu_ppp']] - 12 * coeffs_tot[order_folders['Mnu_pp']] + 32 * coeffs_tot[order_folders["Mnu_p"]] - 12 * coeffs_tot[order_folders['fiducial']]) / (12 * COSMOPAR[i][5]) - \
            (coeffs_tot[order_folders["Mnu_pp"]] - 4 * coeffs_tot[order_folders['Mnu_p']] - 3 * coeffs_tot[order_folders['fiducial']]) / (COSMOPAR[i][5]) + \
            (coeffs_tot[order_folders["Mnu_ppp"]] - coeffs_tot[order_folders['fiducial']]) / COSMOPAR[i][5]
        assert derivates[order_dimension['Mnu']].all() != 0, "Derivates of neutrino mass is null"
    elif "Ob" in i:
        derivates[order_dimension['Ob']] = \
            (coeffs_tot[order_folders[i+"2_p"]]-coeffs_tot[order_folders[i+"2_m"]]) \
            / (2 * VarCosmoPar['d_'+i+"2"] * fiducial_vals[i] )
        assert derivates[order_dimension['Ob']].all() != 0, "Derivates of Omaga barion is null"

fiducial_coeffs = []
with open(root + "/fiducial_coefficients_30_30_1000.wst", 'rb') as Ff:
    while True:
        try:
            fiducial_coeffs.append(pickle.load(Ff))
        except EOFError:
            break

fiducial_coeffs_avg = np.average(fiducial_coeffs, axis = 0)
assert np.shape(fiducial_coeffs_avg) == (75,)

CorrMat = correlation_matrix(fiducial_coeffs)
assert np.linalg.det(CorrMat) != 0, "Singular correlation matrix!"

# HARTLAP matrix from covariance matrix
H = Hartlap(CorrMat, n_realiz)
assert np.shape(H) == (75, 75)

# FISHER matrix
Fi = np.zeros((7,7))
for a in range(7):
    for b in range(7):
        Fi[a, b] = np.sum(derivates[a] * H * derivates[b])

assert np.shape(Fi) == (7, 7)
assert np.linalg.det(Fi) != 0, "Singular Fisher matrix!"

# CONSTRAINS
import scipy as sp
inverse = np.linalg.inv(Fi)
results = []
for i in range(len(inverse)):
    results.append(inverse[i, i])
with open("/home/riccardo/results_no_diagonalizing.txt", 'wb') as res:
    pickle.dump(results, res)