import sys
sys.path.insert(1, './MyFunc')
from CalcWST import HaloWST_f

import os
import pickle

# library fpr progress bar
# use 'from tqdm.auto import tqdm' for both terminal and notebook 
from tqdm import tqdm

# define desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# define output name files with coefficients 
Ff = '_first_order'
Sf = '_second_order'

# define root path where to find hale catalogues 
root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/FoF/'

# choose cosmologies 
folders = ['fiducial']

# loop over cosmologies, calculate and create file WST coeff
for folder in folders:

    # delete existing file, want a new one (not extending it)
    if os.path.exists(folder+Ff):
        os.remove(folder+Ff)
    if os.path.exists(folder+Sf):
        os.remove(folder+Sf)
    
    # loop over the different realizations
    for i in tqdm(range(2)):
        snapdir = root + folder +'/%d'%i
        HaloWST_f(folder+Ff, folder+Sf, snapdir)

first_order_coeffs = []
second_order_coeffs = []

# for folder in folders:
#     for i in range(350):
#         with open(folder+Ff, 'rb') as Ff:
#             while True:
#                 try:
#                     first_order_coeffs.append(pickle.load(Ff))
#                     # do things
#                 except EOFError:
#                     break
#                 # possible
#                 # else:
#                 # ...

# for folder in folders:
#     for i in range(350):
#         with open(folder+Sf, 'rb') as Sf:
#             while True:
#                 try:
#                     second_order_coeffs.append(pickle.load(Sf))
#                     # do things
#                 except EOFError:
#                     break
#                 # possible
#                 # else:
#                 # ...