import numpy as np
import getopt
from tqdm import tqdm
import os
import pickle

import sys
sys.path.insert(1, './MyFunc')
from MyFunc.myDict import order_folders, order_dimension, COSMOPAR, VarCosmoPar, fiducial_vals, cosmological_pars
from MyFunc.name_parser import info_name, cosmo_parser
from MyFunc.Fisher import correlation_matrix, Hartlap, JacobCosmPar
# from CalcWST import HaloWST_f, HaloWST_one_f

# togheter = True
# print(sys.argv[1:])
# info = info_name(sys.argv[1:])
# N_hgrid = info[0]       # number of cells per dimension of halo distribution
# N_WSTgrid = info[1]     # number of cells per dimension of WST evaluation
# n_realiz = info[2]      # number of realization used

# DEFINE file WST coeff parameters
root = './WST-files-easy'
N_hgrid = 256        # number of cells per dimension of halo distribution
N_WSTgrid = 256      # number of cells per dimension of WST evaluation
n_realiz = 350       # number of realization used
togheter = True

# DEFINE desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# DEFINE output suffix name files with coefficients 
Fif = '_first_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'
Sef = '_second_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(n_realiz)+'.wst'

# INITIALIZE useful arrays
# folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
#            'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', \
#            'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']
# cosmologies = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
#            'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', \
#            'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']
folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
           'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', \
           'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']
cosmologies = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
           'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p', \
           'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']

fiducial_coeffs = []
zeldovich_coeffs = []


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
    # # root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/'
    # coeffs_tot = []       # array containing arrays of WST coeffs per cosmology
    # # print("\n    IN THIS ELSE:\n")
    # # CICLE over all the cosmologies
    # for name_file in cosmologies:
    #     coeffs_cosm = []
    #     in_realizations = os.listdir(root)
    #     print("in realizations:\n", in_realizations, "\n")
    #     # print("\n", os.listdir("./"), "\n")
    #     # READ all coefficients of all realizations per cosmology
    #     for i in range(len(in_realizations)):
    #         with open(root+"/"+in_realizations[i], 'rb') as Ff:
    #             print("File name: ", Ff)
    #             while True:
    #                 try:
    #                     # create matrix whose first index refers to the realization
    #                     # the second to the i-th coefficient
    #                     ## coeffs_cosm[i] = pickle.load(Ff)
    #                     coeffs_cosm.append(pickle.load(Ff))
    #                     if "fiducial" in name_file:
    #                         ## fiducial_coeffs[i] = coeffs_cosm[i]
    #                         fiducial_coeffs.append(coeffs_cosm[i])
    #                 except EOFError:
    #                     break
    #     # USING average value per coefficient in cosmology
    #     # print("    COEFF COSMO:\n", np.size(coeffs_cosm), "\n")
    #     ## coeffs_tot[order_folders[name_file]] = np.average(coeffs_cosm, axis=0)
    #     coeffs_tot.append( np.average(coeffs_cosm, axis=0) )
 
   # coeffs_tot = []
    # coeffs_tot = np.zeros((len(cosmologies), n_realiz, 75))
    coeffs_tot = np.zeros((len(cosmologies), 75))
    files_to_read = os.listdir(root)
    
    # # CICLE over cosmologies
    # for i in range(len(files_to_read)):
    #     coeffs_cosm = []
        
    #     # READ all the i-th file
    #     with open(root + "/" + files_to_read[i], 'rb') as Ff:
    #         assert cosmologies[i] in files_to_read[i]
            
    #         cosmo = cosmo_parser(files_to_read[i])
    #         assert cosmo in files_to_read[i]

    #         index = order_folders[cosmo]

    #         while True:
    #             try:
    #                 if "fiducial" not in files_to_read[i] and "zeldovich" not in files_to_read[i]:
    #                     # coeffs_cosm.append(pickle.load(Ff))
    #                     coeffs_cosm[index] = pickle.load(Ff)
    #                 elif "fiducial" in files_to_read[i]:
    #                     fiducial_coeffs[index] = pickle.load(Ff)
    #                 elif "zeldovich" in files_to_read[i]:
    #                     fiducial_coeffs[index] = pickle.load(Ff)
    #                 else:
    #                     assert False, "   Error in assegnating cosmology"
    #             except EOFError:
    #                 break
    #     # USING average  value per coefficient in cosmology
    #     coeffs_tot.append( np.average(coeffs_cosm, axis=0) )

    for i in range(len(files_to_read)):
        coeffs_cosm = []
        file_reading = files_to_read[i]

        cosmo = cosmo_parser(file_reading)
        assert cosmo in file_reading
        print("COSMO KEY: ", cosmo)
        index = order_folders[cosmo]
        
        if "fiducial" not in file_reading and "zeldovich" not in file_reading:
            with open(root + "/" + file_reading, 'rb') as Ff:
                while True:
                    try:
                        # coeffs_cosm.append(pickle.load(Ff))
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
                        # coeffs_cosm.append(pickle.load(Ff))
                        zeldovich_coeffs.append(pickle.load(Ff))
                    except EOFError:
                        break
        else:
            assert False, "\n   ERROR in reading WST files, cosmology can't be propely interpreted.\n"

        # USING average  value per coefficient in cosmology
        if "zeldovich" not in file_reading:
            coeffs_tot[index] = np.average(coeffs_cosm, axis=0)
        else:
            coeffs_tot[index] = np.zeros(np.shape(coeffs_cosm))
# print("Shape -> coeffs_tot: ", np.shape(coeffs_tot))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FISHER MATRIX

derivates = np.zeros((len(cosmological_pars), len(coeffs_tot[0])))
n_seen = 0

# EVALUATE derivates, check for neutrino mass (different formulae)
# for i in folders:
#     n = order_folders[i]

#     if n == n_seen:
#         continue
#     else:
#         n_seen = n
    
#     # if   i == 'Mnu_p':   derivates[order_dimension['Mnu']] += (coeffs_tot[order_folders['Mnu_ppp']] - 12 * coeffs_tot[order_folders['Mnu_pp']] + 32 * coeffs_tot[n] - 12 * coeffs_tot[order_folders['zeldovich']]) / (12 * COSMOPAR[i][5])
#     # elif i == 'Mnu_pp':  derivates[order_dimension['Mnu']] += - (coeffs_tot[n] - 4 * coeffs_tot[order_folders['Mnu_p']] - 3 * coeffs_tot[order_folders['zeldovich']]) / (COSMOPAR[i][5])
#     # elif i == 'Mnu_ppp': derivates[order_dimension['Mnu']] += (coeffs_tot[n] - coeffs_tot[order_folders['zeldovich']]) / COSMOPAR[i][5]
#     if   i == 'Mnu_p':   derivates[order_dimension['Mnu']] += (coeffs_tot[order_folders['Mnu_ppp']] - 12 * coeffs_tot[order_folders['Mnu_pp']] + 32 * coeffs_tot[n] - 12 * coeffs_tot[order_folders['fiducial']]) / (12 * COSMOPAR[i][5])
#     elif i == 'Mnu_pp':  derivates[order_dimension['Mnu']] += - (coeffs_tot[n] - 4 * coeffs_tot[order_folders['Mnu_p']] - 3 * coeffs_tot[order_folders['fiducial']]) / (COSMOPAR[i][5])
#     elif i == 'Mnu_ppp': derivates[order_dimension['Mnu']] += (coeffs_tot[n] - coeffs_tot[order_folders['fiducial']]) / COSMOPAR[i][5]
#     elif "zeldovich" not in i:
#         coms = i[:len(i)-2]
#         assert not (coeffs_tot[n+1] == coeffs_tot[n]).all(), "THE COEFFICIENTS ARE EQUAL BETWEEN COSMOLOGIES"
#         # print("Shape -> derivates: ", np.shape(derivates))
#         # print("Shape -> coeffs_tot: ", np.shape(coeffs_tot))
#         # print("Shape -> coeffs_tot[i]: ", np.shape(coeffs_tot[n]))
#         # assert False, "BREAK before error"
#         derivates[order_dimension[coms]] = (coeffs_tot[n+1] - coeffs_tot[n]) / (2 * VarCosmoPar['d_'+coms] * fiducial_vals[coms] )
#         n_seen += 1

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
print("shape(fiducial_coeffs_avg): ", np.shape(fiducial_coeffs_avg))
assert np.shape(fiducial_coeffs_avg) == (75,)

print("\nfiducial_coeffs_avg:\n", fiducial_coeffs_avg)
print("\nRESULTS:", np.shape(derivates), "\n")#, derivates, "\n")
# exit()

CorrMat = correlation_matrix(fiducial_coeffs)
print(CorrMat)
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

print(Fi)
assert np.linalg.det(Fi) != 0, "Singular Fisher matrix!"

# CONSTRAINS
import scipy as sp
inverse = np.linalg.inv(Fi)
results = []
for i in range(len(inverse)):
    results.append(inverse[i, i])

with open("results_no_diagonalizing.txt", 'wb') as res:
    pickle.dump(results, res)

print("\nRESULTS:\n", results, "\n")
# exit()
constrains = (sp.linalg.eig(inverse))[0]
constrains = constrains ** 0.5
print("\nAAA", (constrains), "\n")

with open("results_diagonalizing.txt", 'wb') as res:
    pickle.dump(constrains, res)