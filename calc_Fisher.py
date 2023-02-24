import numpy as np
import getopt
from tqdm import tqdm
import os
import pickle
import sys
#sys.path.insert(1, './MyFunc')
from MyFunc.myDict import order_folders
# from CalcWST import HaloWST_f, HaloWST_one_f

togheter = False
N_hgrid = 128       # number of cells per dimension of halo distribution
N_WSTgrid = 128     # number of cells per dimension of WST evaluation
n_realiz = 350      # number of realization used

# define desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# define output name files with coefficients 
# Fif = '_first_order.wst'
# Sef = '_second_order.wst'
Fif = '_first_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
Sef = '_second_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
filename = '_coefficients_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'

folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
            'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', \
            'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']

if togheter == True:
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
    coeffs_tot = []         # array containing 
    sigma_coeffs = []
    Cov = []
    for folder in folders:
        coeffs_cosm = []
        sigma = []

        # read all coefficients of all realizations per cosmology
        for i in range(n_realiz):
            with open(folder+filename, 'rb') as Ff:
                while True:
                    try:
                        # create matrix whose first index refers to the realization
                        # the second to the i-th coefficient
                        coeffs_cosm[i] = pickle.load(Ff)
                    except EOFError:
                        break
        
        sigma_coeffs[order_folders[folder]] = np.std(coeffs_cosm, axis=0)
        coeffs_tot[order_folders[folder]] = np.average(coeffs_cosm, axis=0)
        Cov[order_folders[folder]] = np.cov(coeffs_tot)

# ora devo stimare le derivate per calcolare la matrice di Fisher
# ogni elemento della matrice di F. ha fissi i parametri cosmologici e somma su
# tutte le possibili diverse permutazioni dei coeff WST.
# Come devo però trattare le derivate? Le varie cosmologie disponibili hanno tutte
# almeno un parametro cosmologico che devia da quella fiduciale o in eccesso o in
# difetto.
# > IDEA: calcolo i rapporti incrementali di tutte le cosmologie non fiduciali con
# quella fiduciale e poi ne faccio la media, perché utilizzo la matrice di
# covarianza della fiduciale e sono interessato ai costrains sui parametri
# cosmologici della stessa.
# > OSS: quando faccio la media, devo dividere per il numero totale di rapporti
# incrementali che calcolo o solo quelli che mi danno un effettivo valore (ossia
# quelli che hanno parametri cosmologici diversi)?
# > DOMANDA: a questo punto non potrei fare diretamente il rapporto incrementale
# tra le cosmologie che hanno il parametro cosmologico in considerazione una
# aumentato e l'altra diminuito (sempre rispetto alla fiduciale)

from MyFunc.Fisher import JacobCosmPar, Hartlap

derivates = np.zeros((len(order_folders), len(coeffs_tot[0]), len(coeffs_cosm[0])))

for i in range(len(order_folders)):
    if i != order_folders['fiducial']:
        derivates[i] = JacobCosmPar(coeffs_tot[order_folders['fiducial']], coeffs_tot[i], coeffs_cosm[order_folders['fiducial']], coeffs_cosm[i])
    else:
        derivates[i] = 0
        # continue
# matrix of average of derivates
D = np.average(derivates, axis = 0)
# Hartlap matrix from covariance matrix
H = Hartlap(Cov)
# Fisher matrix: scalar product between  
# F = np.matmul(D, np.matmul(H, D))
F = np.zeros((len()))