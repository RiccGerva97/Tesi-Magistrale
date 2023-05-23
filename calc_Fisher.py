import numpy as np
import getopt
from tqdm import tqdm
import os
import pickle

import sys
sys.path.insert(1, './MyFunc')
from MyFunc.myDict import order_folders, order_dimension, COSMOPAR, VarCosmoPar, fiducial_vals
from MyFunc.name_parser import info_name
# from CalcWST import HaloWST_f, HaloWST_one_f

# togheter = True
# print(sys.argv[1:])
# info = info_name(sys.argv[1:])
# N_hgrid = info[0]       # number of cells per dimension of halo distribution
# N_WSTgrid = info[1]     # number of cells per dimension of WST evaluation
# n_realiz = info[2]      # number of realization used

# DEFINE file WST coeff parameters
N_hgrid = 256        # number of cells per dimension of halo distribution
N_WSTgrid = 256      # number of cells per dimension of WST evaluation
n_realiz = 350     # number of realization used
togheter = True

# DEFINE desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# DEFINE output suffix name files with coefficients 
Fif = '_first_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
Sef = '_second_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
filename = '_coefficients_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'

# INITIALIZE useful arrays
folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
           'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', \
           'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']
cosmologies = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
           'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', \
           'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']

fiducial_coeffs = []


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DERIVATES EVALUATION

# CHECK if coefficients of 1° and 2° order are togheder or not
if togheter == False:
    first_order_coeffs = 0
    second_order_coeffs = []

    for folder in folders:
        for i in range(n_realiz):
            Ff = open(folder+Fif, 'rb')
            Sf = open(folder+Sef, 'rb')
            while True:
                try:
                    first_order_coeffs.append(pickle.load(Ff))
                    second_order_coeffs.append(pickle.load(Sf))
                except EOFError:
                    break

else:
    # root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/'
    root = './WST-files'
    coeffs_tot = []         # array containing arrays of WST coeffs per cosmology

    # CICLE over all the cosmologies
    for name_file in cosmologies:
        coeffs_cosm = []
        in_realizations = os.listdir(root)

        # READ all coefficients of all realizations per cosmology
        for i in range(len(in_realizations)):
            with open(in_realizations[i], 'rb') as Ff:
                while True:
                    try:
                        # create matrix whose first index refers to the realization
                        # the second to the i-th coefficient
                        coeffs_cosm[i] = pickle.load(Ff)
                        if "fiducial" in name_file:
                            fiducial_coeffs[i] = coeffs_cosm[i]
                    except EOFError:
                        break
        # USING average value per coefficient in cosmology
        coeffs_tot[order_folders[name_file]] = np.average(coeffs_cosm, axis=0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FISHER MATRIX

from MyFunc.Fisher import JacobCosmPar, Hartlap

derivates = np.zeros((len(order_dimension), len(coeffs_tot[0]), len(coeffs_cosm[0])))

n_seen = 0

# EVALUATE derivates, check for neutrino mass (different formulae)
for i in folders:
    n = order_folders[i]

    if n == n_seen:
        continue
    else:
        n_seen = n
    
    if i == 'Mnu_p':
        derivates[order_dimension['Mnu']] = (coeffs_tot[order_folders['Mnu_ppp']] - 12 * coeffs_tot[order_folders['Mnu_pp']] + 32 * coeffs_tot[n] - 12 * coeffs_tot[order_folders['fiducial']]) / (12 * COSMOPAR[i][5])
        n_seen += 1
    elif i == 'Mnu_pp':
        derivates[order_dimension['Mnu']] = - (coeffs_tot[n] - 4 * coeffs_tot[order_folders['Mnu_p']] - 3 * coeffs_tot[order_folders['fiducial']]) / (COSMOPAR[i][5])
        n_seen += 1
    elif i == 'Mnu_ppp':
        derivates[order_dimension['Mnu']] = (coeffs_tot[n] - coeffs_tot[order_folders['fiducial']]) / COSMOPAR[i][5]
        n_seen += 1
    else:
        coms = i[:len(i)-2]   
        derivates[order_dimension[coms]] = (coeffs_tot[n+1] - coeffs_tot[n]) / (2 * VarCosmoPar['d_'+coms] * fiducial_vals[coms] )
        n_seen += 1
 
CovMat = np.cov(derivates[order_dimension['fiducial']])

# HARTLAP matrix from covariance matrix
H = Hartlap(CovMat, n_realiz)

# FISHER matrix
F = np.dot(derivates*np.dot(H, derivates))

import scipy as sp
inverse = np.linalg.inv(F)
constrains = (sp.linalg.eig(np.linalg.inv(F)))**0.5