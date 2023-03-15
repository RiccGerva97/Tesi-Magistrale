import numpy as np
import getopt
from tqdm import tqdm
import os
import pickle
import sys
sys.path.insert(1, './MyFunc')
from MyFunc.myDict import order_folders, order_dimension, COSMOPAR, VarCosmoPar, fiducial_vals
# from CalcWST import HaloWST_f, HaloWST_one_f

togheter = True
N_hgrid = 256       # number of cells per dimension of halo distribution
N_WSTgrid = 256     # number of cells per dimension of WST evaluation
n_realiz = 350      # number of realization used

# define desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# define output name files with coefficients 
Fif = '_first_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
Sef = '_second_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
filename = '_coefficients_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'

folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
           'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', \
           'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']

# Ob_ cosmologies haven't standard realization
# => only use to generate derivates
# 
# w_ cosmologies only have standard generalization
# 
# HARTLAP matrix:
# use fiducial cosmology to evaluate it
# 
# FISHER matrix:
# - use precedent Hartlap matrix
# - use derivates calculated as:
#   ( S(C_p)-S(C_m) ) / ( 2d*C_par)

# if togheter == True:

if togheter == False:
    first_order_coeffs = 0
    second_order_coeffs = []

    # for folder in folders:
    #     for i in range(350):
    #         with open(folder+Fif, 'rb') as Ff:
    #             while True:
    #                 try:
    #                     first_order_coeffs.append(pickle.load(Ff))
    #                 except EOFError:
    #                     break

    # for folder in folders:
    #     for i in range(350):
    #         with open(folder+Sef, 'rb') as Sf:
    #             while True:
    #                 try:
    #                     second_order_coeffs.append(pickle.load(Sf))
    #                 except EOFError:
    #                     break

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
    root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/'
    coeffs_tot = []         # array containing arrays of WST coeffs per cosmology
    # sigma_coeffs = []
    Cov = []
    for folder in folders:
        coeffs_cosm = []
        # sigma = []
        in_realizations = os.listdir(root+folder)
        # read all coefficients of all realizations per cosmology
        for i in range(in_realizations):
            with open(folder+filename, 'rb') as Ff:
                while True:
                    try:
                        # create matrix whose first index refers to the realization
                        # the second to the i-th coefficient
                        coeffs_cosm[i] = pickle.load(Ff)
                    except EOFError:
                        break
        
        #sigma_coeffs[order_folders[folder]] = np.std(coeffs_cosm, axis=0)
        coeffs_tot[order_folders[folder]] = np.average(coeffs_cosm, axis=0)
        
        # CONTROLLA
        if 'Ob_' not in folder:
            Cov[order_folders[folder]] = np.cov(coeffs_tot[0:500])

# VEDI `Pensieri_oziosi.md` 

from MyFunc.Fisher import JacobCosmPar, Hartlap

derivates = np.zeros((len(order_dimension), len(coeffs_tot[0]), len(coeffs_cosm[0])))

n_seen = 0

for i in folders:
    n = order_folders[i]

    if n == n_seen:
        continue
    else:
        n_seen = n
    
    if i == 'Mnu_p':
        derivates[order_dimension['Mnu']] = (coeffs_tot[order_folders['Mnu_ppp']] - 12 * coeffs_tot[order_folders['Mnu_pp']] + 32 * coeffs_tot[n] - 12 * coeffs_tot[order_folders['fiducial']]) / (12 * COSMOPAR[i][5])
        n_seen += 1
        continue
    if i == 'Mnu_pp':
        derivates[order_dimension['Mnu']] = - (coeffs_tot[n] - 4 * coeffs_tot[order_folders['Mnu_p']] - 3 * coeffs_tot[order_folders['fiducial']]) / (COSMOPAR[i][5])
        n_seen += 1
        continue
    if i == 'Mnu_ppp':
        derivates[order_dimension['Mnu']] = (coeffs_tot[n] - coeffs_tot[order_folders['fiducial']]) / COSMOPAR[i][5]
        n_seen += 1
        continue
    
    coms = i[:len(i)-2]
    if "Ob" not in i:      
        derivates[order_dimension[coms]] = (coeffs_tot[n+1] - coeffs_tot[n]) / (2 * VarCosmoPar['d_'+coms] * fiducial_vals[coms] )
        n_seen += 1

    if "Ob" in i:
        derivates[order_dimension[coms]] += (coeffs_tot[n+1] - coeffs_tot[n]) / (2 * VarCosmoPar['d_'+coms] * fiducial_vals[coms] )
        n_seen += 1

# SBALGIATO, SOLO CONCETTUALE: FARE POI LA MEDIA  
derivates[order_dimension["Ob"]] /= 2

    
    

    

for i in range(len(order_folders)):
    if i != order_folders['fiducial']:
        # primo indice sulle cosmologie, il secondo suicoefficienti
        derivates[i] = JacobCosmPar(coeffs_tot[order_folders['fiducial']], coeffs_tot[i], coeffs_cosm[order_folders['fiducial']], coeffs_cosm[i])
    else:
        derivates[i] = 0
        # continue
# matrix of average of derivates
D = np.average(derivates, axis = 0)
# Hartlap matrix from covariance matrix
H = Hartlap(Cov, 500)
# Fisher matrix: scalar product between  
# F = np.matmul(D, np.matmul(H, D))
F = np.zeros((len(1)))