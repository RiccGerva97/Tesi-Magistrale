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
# Fif = '_first_order.wst'
# Sef = '_second_order.wst'
Fif = '_first_order.wst'
Sef = '_second_order.wst'


# define root path where to find hale catalogues 
root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/FoF/'

# choose cosmologies 
folders = ['fiducial']

# loop over cosmologies, calculate and create file WST coeff
for folder in folders:

    # delete existing file, want a new one (not extending it)
    if os.path.exists(folder+Fif):
        os.remove(folder+Fif)
    if os.path.exists(folder+Sef):
        os.remove(folder+Sef)
    
    # loop over the different realizations
    for i in tqdm(range(2)):
        snapdir = root + folder +'/%d'%i
        HaloWST_f(folder+Fif, folder+Sef, snapdir)

first_order_coeffs = []
second_order_coeffs = []

# for folder in folders:
#     for i in range(350):
#         with open(folder+Fif, 'rb') as Ff:
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
#         with open(folder+Sef, 'rb') as Sf:
#             while True:
#                 try:
#                     second_order_coeffs.append(pickle.load(Sf))
#                     # do things
#                 except EOFError:
#                     break
#                 # possible
#                 # else:
#                 # ...