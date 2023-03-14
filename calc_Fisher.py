import numpy as np
import getopt
from tqdm import tqdm
import os
import pickle
import sys
#sys.path.insert(1, './MyFunc')
from MyFunc.myDict import order_folders, COSMOPAR, VarCosmoPar, fiducial_vals
# from CalcWST import HaloWST_f, HaloWST_one_f

togheter = False
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

# NOVITA': i ricercatori Quijote per calcolare le derivate di un parametro fanno:
# d/dx S_i = (S_i(x+dx)-S_i(x-dx)) / 2dx
# quindi poteri pensare di valutare le deirvate facendo le differenze tra 
# cosmologie _p e _m (dei coefficienti e dei parametri)
# Conviene calcolare già gli step o utilizzare le percentuali come da paper?
# NOTA: essendoci 4 variazioni sulla densità di barioni, considero solo le coppie 
# (+, -) e (++, --) o posso/conviene calcolare anche le altre (aggiustanto la formula),
# che sono (++, -), (+, --), (++, +), (-, --)?
# Sono sensate solo quelle che hanno i termini fiduciali all'interno? E basterebbe
# aggiustare o bisogna aggingere dei possibili pesi?

# PENSIERI OZIOSI
# In quasi tutte le cosmologie ci sono tre tipologie di realizzazioni:
# - standard -> 500
# - fisse -> 250
# - fisse accoppiate -> 250
# cioè dipende come vengono generati (aka con quale distribuzione vengono calcolati) i
# parametri iniziali delle simulazioni.
# Il sig. Navarro ci informa che possono essere utulizzate tutte e 1000 solo per il
# computo delle derivate, mentre per quello della matrice di covarianza solo quelle standard.

# Ora ho due strade:
# a) usare 350/500 standard e basta;
# b) usare standard e fisse (/accoppiate) -> quante? Perché l'importante è usarne >= 350 standard
#     per avere una matrice di covar.sufficientemente bendefinita
# Priblema:
# 1) "Ob_" ha solo realizzazioni non standard -> posso supperire con "Ob2_"
# 2) "w_" ha solo realizzazioni standard

# Come posso mettere insieme a), b) e 1), 2)?
# La facile soluzione sarebbe calcolare il tutto solo con realizzazioni standard e non usare
# le cosmologie varianti "Ob_".

# SOLUZIONE PIU' ARTICOLATA
# Si potrebbe invece pensare di calcolare la matrice di covarianza con le realizzazioni standard,
# le derivate anche con quelle fisse.
# Bisogna però:
# - pensare a come (e se si deve) riportare che le derivare -> Fisher per cosmologie "w_"
# hanno una precisione minore;
# - come "unire" le derivate fatte su variazione di Omega_b (perché è quella con ++, +, -, --) 


from MyFunc.Fisher import JacobCosmPar, Hartlap

derivates = np.zeros((len(order_folders), len(coeffs_tot[0]), len(coeffs_cosm[0])))

n_seen = 0
for i in folders:
    n = order_folders[i]

    if n == n_seen:
        continue

    if i == 'Mnu_p':
        derivates[n] = (coeffs_tot[order_folders['Mnu_ppp']] - 12 * coeffs_tot[order_folders['Mnu_pp']] + 32 * coeffs_tot[n] - 12 * coeffs_tot[order_folders['fiducial']]) / (12 * COSMOPAR[i][5])
        continue
    if i == 'Mnu_pp':
        derivates[n] = - (coeffs_tot[n] - 4 * coeffs_tot[order_folders['Mnu_p']] - 3 * coeffs_tot[order_folders['fiducial']]) / (COSMOPAR[i][5])
        continue
    if i == 'Mnu_ppp':
        derivates[n] = (coeffs_tot[n] - coeffs_tot[order_folders['fiducial']]) / COSMOPAR[i][5]
        continue
    
    if "Ob_" not in i:
        derivates[n] = (coeffs_tot[n+1] - coeffs_tot[n]) / (2 * VarCosmoPar['d_'+i[:len(i)-2]] * fiducial_vals[i[:len(i)-2]] )
    
    

    

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
H = Hartlap(Cov)
# Fisher matrix: scalar product between  
# F = np.matmul(D, np.matmul(H, D))
F = np.zeros((len()))