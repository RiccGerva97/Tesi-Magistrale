import sys, os
import numpy as np
import numpy.ma as ma
import emcee
import corner
import torch
from nbodykit.lab import *
import nbodykit
import pickle
import matplotlib.pyplot as plt
from kymatio.torch import HarmonicScattering3D
from kymatio.scattering3d.backend.torch_backend import TorchBackend3D
#from joblib import Parallel, delayed, parallel_backend

cosmo = cosmology.Cosmology(h=0.6736).match(Omega0_m=0.3152)

def read_sim_data(filename):
    ''' Read the random simulation catalogues from CSV '''
    sim_cat = nbodykit.lab.CSVCatalog(os.path.join(filename),\
        names=['RA', 'DEC', 'Z', 'MSTAR', 'NZ', 'BIAS', 'VETO_FLAG', 'FIBER_COLLISION'])
    #print('sim_cat.columns = ', sim_cat.columns)
    sim_cat = sim_cat[(sim_cat['Z'] > 0.46) & (sim_cat['Z'] < 0.60)]
    sim_cat = sim_cat[(sim_cat['VETO_FLAG'] > 0)]
    sim_cat['WEIGHT_FKP'] = 1./(1. + 10000.*sim_cat['NZ']);
    sim_cat['Weight'] = sim_cat['VETO_FLAG']*sim_cat['FIBER_COLLISION']
    return sim_cat

def read_sim_ran(filename):
    ''' Read the simulation catalogues from CSV '''
    ran_cat = nbodykit.lab.CSVCatalog(os.path.join(filename),\
        names=['RA', 'DEC', 'Z', 'NZ', 'BIAS', 'VETO_FLAG', 'FIBER_COLLISION'])
    #print('ran_cat.columns = ', ran_cat.columns)
    ran_cat = ran_cat[(ran_cat['Z'] > 0.46) & (ran_cat['Z'] < 0.6)]
    ran_cat = ran_cat[(ran_cat['VETO_FLAG'] > 0)]
    ran_cat['WEIGHT_FKP'] = 1./(1. + 10000.*ran_cat['NZ']);
    ran_cat['Weight'] = ran_cat['VETO_FLAG']*ran_cat['FIBER_COLLISION']
    print("Random catalogue loaded correctly.")
    return ran_cat


def calc_pk(fkp):
    mesh = fkp.to_mesh(Nmesh=500, nbar='NZ', comp_weight='Weight', fkp_weight='WEIGHT_FKP', window='tsc')
    # Calculate power spectrum (monopole only)
    r = ConvolvedFFTPower(mesh, poles=[0,2], dk=0.01, kmin=0.001)
    return r.poles

def calc_wst(fkp, num, tag):
    print("Calculating mesh and mask...", flush = True)
    mesh_wst = fkp.to_mesh(Nmesh=282, nbar='NZ', fkp_weight='WEIGHT_FKP', comp_weight='Weight', window='tsc')
    data = mesh_wst.preview().astype('float32')
    window = mesh_wst['randoms'].preview().astype('float32')
    mask = ma.masked_where(window!=0, window).mask
    mask = mask[np.newaxis,:,:,:,np.newaxis]

    #print out normalization
    print("Printed out normalization (np.count_nonzero(mask)) to file norm.txt.", flush=True)
    with open('norm.txt', 'a') as f:
        string = tag + "_" + str(num) + ": "+ str(np.count_nonzero(mask)) + "\n"
        f.write(string)
    
    print("Initializing the scattering class...", flush=True)
    S = HarmonicScattering3D(J=4, L=4, shape=(282, 282, 282), sigma_0=0.8, integral_powers=[0.8], mask = mask)
    del mask, window, mesh_wst #to preserve memory and RAM

    print("Calculating the actual coefficients...", flush = True)
    # Calculate the scattering transform.
    Sx = S.scattering(torch.from_numpy(data))
    order_0_s = np.zeros(1)
    order_0_s[0] = (np.abs(data)**0.8).sum()
    del S
    return np.concatenate((order_0_s, torch.flatten(Sx,start_dim=0)))



def calc_pk_parallel(filename, num):
    pk_file = "sims/pk_%s_%d.pickle" % ("NGC", num)
    #print("Power spectrum already existing, let's move on! :)", flush=True)
    # Only calculate power spectra which we don't have on disk
    if not os.path.isfile(pk_file):
        print("Calculating power spectrum!", flush=True)
        sim = read_sim_data(filename)
        sim['Position'] = transform.SkyToCartesian(sim['RA'], sim['DEC'], sim['Z'], cosmo=cosmo)
        randoms_North = read_sim_ran('Patchy-Mocks-Randoms-DR12NGC-COMPSAM_V6C_x50.dat')
        randoms_North['Position'] = transform.SkyToCartesian(randoms_North['RA'], randoms_North['DEC'], randoms_North['Z'], cosmo=cosmo)
        FKP = FKPCatalog(sim, randoms_North, BoxSize=2820)
        del randoms_North, sim
        pk = calc_pk(FKP)
        pickle.dump( pk, open( pk_file, "wb" ) )

def calc_wst_parallel(filename, num, tag):
    wst_file = "sims/wst_%s_%d.pickle" % (tag, num)
    if not os.path.isfile(wst_file):
        print("Loading simulation and randoms...", flush=True)
        sim = read_sim_data(filename)
        sim['Position'] = transform.SkyToCartesian(sim['RA'], sim['DEC'], sim['Z'], cosmo=cosmo)
        if tag == "SGC":
            randoms = read_sim_ran('Patchy-Mocks-Randoms-DR12SGC-COMPSAM_V6C_x50.dat')
        else:
            randoms = read_sim_ran('Patchy-Mocks-Randoms-DR12NGC-COMPSAM_V6C_x50.dat')
        
        randoms['Position'] = transform.SkyToCartesian(randoms['RA'], randoms['DEC'], randoms['Z'], cosmo=cosmo)
        print("Building FKP field...", flush = True)
        FKP = FKPCatalog(sim, randoms, BoxSize=2820)
        wst = calc_wst(FKP, num ,tag)
        pickle.dump( wst, open( wst_file, "wb" ) )


#randoms_South = read_sim_ran('Patchy-Mocks-Randoms-DR12SGC-COMPSAM_V6C_x50.dat')
#randoms_North = read_sim_ran('Patchy-Mocks-Randoms-DR12NGC-COMPSAM_V6C_x50.dat')
#randoms_South['Position'] = transform.SkyToCartesian(randoms_South['RA'], randoms_South['DEC'], randoms_South['Z'], cosmo=cosmo)
#randoms_North['Position'] = transform.SkyToCartesian(randoms_North['RA'], randoms_North['DEC'], randoms_North['Z'], cosmo=cosmo)

if __name__ == "__main__":
    n = sys.argv[1]
    n = int(n)

    path_south = "Patchy-Mocks-DR12SGC-COMPSAM_V6C/Patchy-Mocks-DR12SGC-COMPSAM_V6C_"
    path_north = "Patchy-Mocks-DR12NGC-COMPSAM_V6C/Patchy-Mocks-DR12NGC-COMPSAM_V6C_"

    filename_n = path_north + str(n).zfill(4) + ".dat"
    filename_s = path_south+ str(n).zfill(4) + ".dat"

    print("Calculating wst for NGC", n, flush=True)
    calc_wst_parallel(filename_n, n, "NGC")

    print("Calculating wst for SGC", n, flush=True)
    calc_wst_parallel(filename_s, n, "SGC")

    


    

        
