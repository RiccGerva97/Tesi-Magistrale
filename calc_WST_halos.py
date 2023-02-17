import sys
sys.path.insert(1, './MyFunc')
from CalcWST import HaloWST_f

import os
import pickle

# define desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# define output name files with coefficients 
Ff = 'first_order'
Sf = 'second_order'

# define root path where to find hale catalogues 
root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/'

# choose cosmologies 
folders = ['fiducial']

first_order_coeffs = []
second_order_coeffs = []

# loop over cosmologies
for folder in folders:
    if os.path.exists(folder+Ff):
        os.remove(folder+Ff)
    if os.path.exists(folder+Sf):
        os.remove(folder+Sf)
    
    # loop over the different realizations
    for i in range(350):
        snapdir = root + folder +'/%d'%i
        HaloWST_f(folder+Ff, folder+Sf, snapdir)

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