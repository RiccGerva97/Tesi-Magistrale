import numpy as np
import os
import time
import pickle
import gc
import readfof
import torch

from kymatio.torch import HarmonicScattering3D
from kymatio.scattering3d.backend.torch_backend \
    import TorchBackend3D

from myCIC import cic
import MAS_library as MASL

# library fpr progress bar
    # use 'from tqdm.auto import tqdm' for both terminal and notebook 
from tqdm import tqdm

def HaloWST_one_f_MASL(filename, snapdir, snapnum=2, N_hgrid=256, hlength=1000, N_WSTgrid=256, j=4, l=4, i=-1):
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

    gc.collect()

    if i != -1:
        start = time.time()

    datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = datas.GroupPos/1e3                     # positions in Mpc/h
    mass = datas.GroupMass * 1e10                  # masses in M_sun/h
    dens = np.zeros((N_hgrid,N_hgrid,N_hgrid), dtype=np.float32)
    MASL.MA(pos_h.astype(np.float32), dens, hlength, 'CIC', W = mass.astype(np.float32))
    
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0  

    Sx = HarmonicScattering3D(J=j, L=l, shape=(N_WSTgrid, N_WSTgrid, N_WSTgrid), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))

    # file = open(filename, 'ab')
    # pickle.dump(torch.flatten(Sx,start_dim=0).cpu().detach().numpy(), file)
    # file.close()

    with open('WST-files/'+filename, 'ab') as file:
        pickle.dump(torch.flatten(Sx, start_dim=0).cpu().detach().numpy(), file)
    
    if i != -1:
        print(f"Ended in {time.time() - start} seconds ({i}°)")

def HaloWST(snapdir, snapnum=2, N_hgrid=128, hlength=1000, N_WSTgrid=128, j=4, l=4):
    """Funcion that evaluates Scattering Transform coefficients of first and second order,
    using a halo database from Quijote simulations.

    Arguments:
    - `snapdir` : the tree to the directory containing the datas, STOP before '/groups_';
    - `snapnum` : indicates the choosen redshift (def: 2)
    - `N_hgrid` : number of cells to divide the halos catalogue (def: 128)
    - `hlength` : dimension of the cubic simulation (def: 1000 Mpc/h)
    - `N_WSTgrid` : number of cells to divide the density field, generated by myCIC,
      to calculate WST coefficients (def: 128)
    - `j` : coefficient for scattering transform evaluation (def: 4)
    - `l` : coefficient for scattering transform evaluation (def: 4)

    Returns:
    - touple, whose two elements are:
        * first order scattering transform coefficients
        * second order scattering transform coefficients
    """

    gc.collect()

    datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = datas.GroupPos/1e3                     # positions in Mpc/h
    mass = datas.GroupMass * 1e10                  # masses in M_sun/h
    dens = cic(pos_h, mass, N_hgrid, hlength)
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0  
    # S = HarmonicScattering3D(J=J, L=L, shape=(M, N, O), sigma_0=0.8, integral_powers=[0.8])

#    M, N, O = N_WSTgrid, N_WSTgrid, N_WSTgrid
#    J, L = j, l    
#    Sx = HarmonicScattering3D(J=J, L=L, shape=(M, N, O), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))
    
    Sx = HarmonicScattering3D(J=j, L=l, shape=(N_WSTgrid, N_WSTgrid, N_WSTgrid), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))

    del datas, pos_h, mass, dens

    first_order = []
    second_order = []

    for a in range(l+1):
        for b in range(j+1):
            first_order.append(Sx[b, a, 0])
        second_order.append(Sx[5:,a,0].numpy())

    del Sx

    return (first_order, second_order)

def HaloWST_f(first_file, second_file, snapdir, snapnum=2, N_hgrid=128, hlength=1000, N_WSTgrid=128, j=4, l=4, i=-1):
    """Funcion that evaluates Scattering Transform coefficients of first and second order,
    using a halo database from Quijote simulations.

    Arguments:
    - `first_file`: name of the file conaining WST coefficients of first order
    - `second_file`: name of the file conaining WST coefficients of second order
    - `snapdir` : the tree to the directory containing the datas, STOP before '/groups_';
    - `snapnum` : indicates the choosen redshift (def: 2)
    - `N_hgrid` : number of cells to divide the halos catalogue (def: 128)
    - `hlength` : dimension of the cubic simulation (def: 1000 Mpc/h)
    - `N_WSTgrid` : number of cells to divide the density field, generated by myCIC,
      to calculate WST coefficients (def: 128)
    - `j` : coefficient for scattering transform evaluation (def: 4)
    - `l` : coefficient for scattering transform evaluation (def: 4)
    - `i` : oprional, svariable for print execution time, takes value from iterable object of for loop

    Returns:
    - prints fist and second order scattering coefficients into two different files
    """

    # empty RAM
    gc.collect()

    if i != -1:
        start = time.time()

    datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = datas.GroupPos/1e3                     # positions in Mpc/h
    mass = datas.GroupMass * 1e10                  # masses in M_sun/h
    dens = cic(pos_h, mass, N_hgrid, hlength)
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0  

    Sx = HarmonicScattering3D(J=j, L=l, shape=(N_WSTgrid, N_WSTgrid, N_WSTgrid), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))

    first_order = []
    second_order = []

    for a in range(l+1):
        for b in range(j+1):
            first_order.append(Sx[b, a, 0].numpy())
        second_order.append(Sx[5:,a,0].numpy())

    file_one = open(first_file, 'ab')
    pickle.dump(np.array(first_order), file_one)
    file_one.close()
    
    file_two = open(second_file, 'ab')
    pickle.dump(np.array(second_order), file_two)
    file_two.close()

    if i != -1:
        print(f"Ended in {time.time() - start} seconds ({i}°)")

def HaloWST_one(filename, snapdir, snapnum=2, N_hgrid=128, hlength=1000, N_WSTgrid=128, j=4, l=4, i=-1):
    """Funcion that evaluates Scattering Transform coefficients of first and second order,
    using a halo database from Quijote simulations.

    Arguments:
    - `filename`: name of the file conaining WST coefficients of first and second order
    - `snapdir` : the tree to the directory containing the datas, STOP before '/groups_';
    - `snapnum` : indicates the choosen redshift (def: 2)
    - `N_hgrid` : number of cells to divide the halos catalogue (def: 128)
    - `hlength` : dimension of the cubic simulation (def: 1000 Mpc/h)
    - `N_WSTgrid` : number of cells to divide the density field, generated by myCIC,
      to calculate WST coefficients (def: 128)
    - `j` : coefficient for scattering transform evaluation (def: 4)
    - `l` : coefficient for scattering transform evaluation (def: 4)
    - `i` : oprional, svariable for print execution time, takes value from iterable object of for loop

    Returns:
    - 1D array with all 76 WST coefficients.
    """

    gc.collect()

    if i != -1:
        start = time.time()

    datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = datas.GroupPos/1e3                     # positions in Mpc/h
    mass = datas.GroupMass * 1e10                  # masses in M_sun/h
    dens = cic(pos_h, mass, N_hgrid, hlength)
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0  

    Sx = HarmonicScattering3D(J=j, L=l, shape=(N_WSTgrid, N_WSTgrid, N_WSTgrid), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))

    if i != -1:
        print(f"Ended in {time.time() - start} seconds ({i}°)")

    return torch.flatten(Sx,start_dim=0).cpu().detach().numpy()

def HaloWST_one_f(filename, snapdir, snapnum=2, N_hgrid=128, hlength=1000, N_WSTgrid=128, j=4, l=4, i=-1):
    """Funcion that evaluates Scattering Transform coefficients of first and second order,
    using a halo database from Quijote simulations.

    Arguments:
    - `filename`: name of the file conaining WST coefficients of first and second order
    - `snapdir` : the tree to the directory containing the datas, STOP before '/groups_';
    - `snapnum` : indicates the choosen redshift (def: 2)
    - `N_hgrid` : number of cells to divide the halos catalogue (def: 128)
    - `hlength` : dimension of the cubic simulation (def: 1000 Mpc/h)
    - `N_WSTgrid` : number of cells to divide the density field, generated by myCIC,
      to calculate WST coefficients (def: 128)
    - `j` : coefficient for scattering transform evaluation (def: 4)
    - `l` : coefficient for scattering transform evaluation (def: 4)
    - `i` : oprional, svariable for print execution time, takes value from iterable object of for loop

    Returns:
    - prints fist and second order scattering coefficients into a single files as 1D array.
    """

    gc.collect()

    if i != -1:
        start = time.time()

    datas = readfof.FoF_catalog(snapdir, snapnum, read_IDs=False)
    pos_h = datas.GroupPos/1e3                     # positions in Mpc/h
    mass = datas.GroupMass * 1e10                  # masses in M_sun/h
    dens = cic(pos_h, mass, N_hgrid, hlength)
    dens /= np.mean(dens, dtype=np.float64)
    dens -= 1.0  
    
    Sx = HarmonicScattering3D(J=j, L=l, shape=(N_WSTgrid, N_WSTgrid, N_WSTgrid), sigma_0=0.8, integral_powers=[0.8]).scattering(torch.from_numpy(dens))

    file = open(filename, 'ab')
    pickle.dump(torch.flatten(Sx,start_dim=0).cpu().detach().numpy(), file)
    file.close()
    
    if i != -1:
        print(f"Ended in {time.time() - start} seconds ({i}°)")

def CALCULUS(togheter = True, N_hgrid = 128, N_WSTgrid = 128, n_realiz = 350, Ff = ['fiducial']):
    """Evaluates WST coefficients and print them in one/two files (this is an option) for given foldees
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

    if togheter == True:
        in_realizations = os.listdir(root+folder)
        filename = '_coefficients_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(len(in_realizations))+'.wst'
        
        # loop over cosmologies, calculate and create file WST coeff
        for folder in tqdm(folders):

            # delete existing file, want a new one (not extending it)
            if os.path.exists('../WST-files/'+folder+filename): os.remove(folder+filename)
            
            # for i in range tqdm(range(n_realiz),leave = False):
            for i in tqdm(in_realizations, leave = False):
                # snapdir = root + folder +'/%d'%i
                snapdir = root + folder + '/' + i
                HaloWST_one_f_MASL(folder+filename, snapdir, N_hgrid = N_hgrid, N_WSTgrid = N_WSTgrid)
    else:
        in_realizations = os.listdir(root+folder)

        # define output name files with coefficients 
        Fif = '_first_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(len(in_realizations))+'.wst'
        Sef = '_second_order_'+str(N_hgrid)+"_"+str(N_WSTgrid)+"_"+str(len(in_realizations))+'.wst'


        # loop over cosmologies, calculate and create file WST coeff
        for folder in tqdm(folders):

            # delete existing file, want a new one (not extending it)
            if os.path.exists('../WST-files/'+folder+Fif): os.remove('../WST-files/'+folder+Fif)
            if os.path.exists('../WST-files/'+folder+Sef): os.remove('../WST-files/'+folder+Sef)
            
            # loop over the different realizations
            for i in tqdm(in_realizations, leave=False):
                # snapdir = root + folder +'/%d'%i
                snapdir = root + folder + '/' + i
                HaloWST_f(folder+Fif, folder+Sef, snapdir, N_hgrid = N_hgrid, N_WSTgrid = N_WSTgrid)