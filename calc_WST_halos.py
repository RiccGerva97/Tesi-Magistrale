import sys
sys.path.insert(1, './MyFunc')
from CalcWST import HaloWST_f

import pickle

# define desired redshift
snapnum = 2
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# define output name files with coefficients 
first_file = 'first_order'
second_file = 'second_order'

# define root path where to find hale catalogues 
root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/'

# choose cosmologies 
folders = ['fiducial']

first_order_coeffs = []
second_order_coeffs = []

# loop over cosmologies
for folder in folders:
    # loop over the different realizations
    for i in range(350):
        snapdir = root + folder +'/%d'%i
        HaloWST_f(first_file, second_file, snapdir)

# for i in range(350):
#     with open(first_file, 'rb') as Ff:
#         while True:
#             try:
#                 a = pickle.load(Ff)
#                 # do things
#             except EOFError:
#                 break
#             # possible
#             # else:
#             # ...

# for i in range(350):
#     with open(second_file, 'rb') as Sf:
#         while True:
#             try:
#                 a = pickle.load(Sf)
#                 # do things
#             except EOFError:
#                 break
#             # possible
#             # else:
#             # ...