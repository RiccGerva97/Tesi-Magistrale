import numpy as np
import os, sys
import pickle
import readfof
import torch

from kymatio.torch import HarmonicScattering3D
from kymatio.scattering3d.backend.torch_backend \
    import TorchBackend3D

import MAS_library as MASL

def HaloWST_one_f_MASL(filename, snapdir, snapnum=2, N_hgrid=256, hlength=1000, N_WSTgrid=256, j=4, l=4):
    """Funcion that evaluates Scattering Transform coefficients of first and second order,
    using a halo database from Quijote simulations.
    NB: this function uses `MAS_library.MA()` to generate density matrix, not `myCIC`.

    Arguments:
    - `filename`: name of the file conaining WST coefficients of first and second order
    - `snapdir` : the tree to the directory containing the datas, STOP before '/groups_';
    - `snapnum` : indicates the choosen redshift (def: 2)
    - `N_hgrid` : number of cells to divide the halos catalogue (def: 256)
    - `hlength` : dimension of the cubic simulation (def: 1000 Mpc/h)
    - `N_WSTgrid` : number of cells to divide the density field, generated by myCIC,
      to calculate WST coefficients (def: 256)
    - `j` : coefficient for scattering transform evaluation (def: 4)
    - `l` : coefficient for scattering transform evaluation (def: 4)
    - `i` : oprional, svariable for print execution time, takes value from iterable object of for loop

    Returns:
    - prints fist and second order scattering coefficients into a single files as 1D array.
    """

    # gc.collect()

    datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = datas.GroupPos/1e3                     # positions in Mpc/h
    mass = datas.GroupMass * 1e10                  # masses in M_sun/h
    dens = np.zeros((N_hgrid,N_hgrid,N_hgrid), dtype=np.float32)

    MASL.MA(pos_h.astype(np.float32), dens, hlength, 'CIC', W = mass.astype(np.float32))
    
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0  

    Sx = HarmonicScattering3D(J=j, L=l, shape=(N_WSTgrid, N_WSTgrid, N_WSTgrid), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))

    with open('WST-files/'+filename, 'ab') as file:
        pickle.dump(torch.flatten(Sx, start_dim=0).cpu().detach().numpy(), file)


def CALCULUS(N_hgrid = 256, N_WSTgrid = 256, n_realiz = -1, Ff = ['fiducial', 'h_m', 'h_p',\
                                                                  'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
                                                                  'ns_m', 'ns_p', 'Ob2_m', 'Ob2_p',\
                                                                  'Om_m', 'Om_p', 's8_m', 's8_p',\
                                                                  'w_m', 'w_p']):
    """Evaluates WST coefficients and print them in one/two files (this is an option) for given folders
    using `HaloWST_one_f_MASL`
    """
    
    # define desired redshift
    snapnum = 2
    z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
    redshift = z_dict[snapnum]

    # define root path where to find hale catalogues
    # root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/FoF/'
    root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/'

    # choose cosmologies 
    folders = Ff

    # loop over cosmologies, calculate and create file WST coeff
    for folder in folders:
        if n_realiz < 0:
            in_realizations = os.listdir(root+folder)
            num = len(in_realizations)
        else:
            num = n_realiz
            in_realizations = os.listdir(root+folder)[0:num]

        filename = '_coefficients_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(num)+'.wst'

        # # delete existing file, want a new one (not extending it)
        # if os.path.exists('../WST-files/'+folder+filename): os.remove(folder+filename)
        
        for i in in_realizations:
            snapdir = root + folder + '/' + i
            HaloWST_one_f_MASL(folder+filename, snapdir, N_hgrid = N_hgrid, N_WSTgrid = N_WSTgrid)

if __name__ == "__main__":
    n = sys.argv[1]
    names = n.split(' ', str)[-3:]
    CALCULUS(N_hgrid=256, N_WSTgrid=256, n_realiz=350, Ff = names)