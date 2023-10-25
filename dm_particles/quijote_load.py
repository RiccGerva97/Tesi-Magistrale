import sys, time, os, pickle, traceback
import h5py#, hdf5plugin
import kymatio, readgadget, nbodykit

import numpy as np

from kymatio.torch import HarmonicScattering3D
from readfof import FoF_catalog
from torch import flatten, from_numpy
from datetime import datetime, timedelta

# nbodykit tool to read custom (non-standard) catalogue file type
from nbodykit.io.base import FileType
# nbodykit tool to creae custom subclass od CatalogSource
from nbodykit.source.catalog.file import FileCatalogFactory
from nbodykit.source.catalog import BinaryCatalog
# nbodykit cosmology parameters initialization
from nbodykit.lab import cosmology, FFTPower

from multiprocessing import Process, current_process

# ==== DICTIONARIES ==================================================================

z_dict = {4:0.0,
          3:0.5,
          2:1.0,
          1:2.0,
          0:3.0}

# ==== FUNCTIONS =====================================================================

def delta_time(T):
    return str(round((time.time()-T)/60, 3))

def update_log(a, log_name_now):
    if not type(a) == str: a = str(a) 
    with open('/home/jovyan/AA_Ricc/log/'+log_name_now, 'a') as f:
        f.write("\n"+a)

def HaloWST_one_f_MASL(S, filename, snapdir, i, \
                       snapnum=2, N_grid=256, N_mesh=512, \
                       hlength=1000, j=4, l=4, \
                       log_name="a.log"):
    strt = time.time()
    print("in evaluation")
    update_log("  in evaluation", log_name_now=log_name)
    # initialize folder indications
    snapshot = snapdir + '/snapdir_000/snap_000'
    ptype    = [1]

    # ==== read datas and cosmologiy's info =============
    header   = readgadget.header(snapshot)
    BoxSize  = header.boxsize/1e3  #Mpc/h
    Nall     = header.nall         #Total number of particles
    Masses   = header.massarr*1e10 #Masses of the particles in Msun/h
    Omega_m  = header.omega_m      #value of Omega_m
    Omega_l  = header.omega_l      #value of Omega_l
    h        = header.hubble       #value of h
    redshift = header.redshift     #redshift of the snapshot
    H_z      = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#Value of H(z) in km/s/(Mpc/h)

    # read positions, velocities and IDs of the particles
    pos = readgadget.read_block(snapshot, "POS ", ptype)/1e3 #positions in Mpc/h
    # vel = readgadget.read_block(snapshot, "VEL ", ptype)

    with open('./data_source.dat', "wb") as ff:
        # pos_h.tofile(ff); pos_rsd.tofile(ff); vel.tofile(ff); mass.tofile(ff)
        pos.tofile(ff); np.full(len(pos), Masses[1], dtype=np.float32).tofile(ff)
        ff.seek(0)
    
    # create catalog obj
    binCat = BinaryCatalog(ff.name, dtype_cust)

    ## ========= WST claulus =================================
    update_log("    beginning WST",\
               log_name_now=log_name)
    start_wst = time.time()

    mesh_wst = binCat.to_mesh(resampler='tsc', Nmesh=N_grid,
                              compensated=True,  # deconvolving
                              interlaced=True,   # antialiasing
                              position='Position', weight="Mass",
                              BoxSize=BoxSize
                              )
    # initialize density
    dens = mesh_wst.preview().astype('float32')

    update_log("        finished MASL.MA", log_name_now=log_name)

    Sx = S.scattering(from_numpy(dens))
    with open('/home/jovyan/AA_Ricc/Results/WST-files/' + \
              filename.replace("_coefficients_", "_coefficients_M_real_"), 'ab') as file:
        pickle.dump(flatten(Sx, start_dim=0).cpu().detach().numpy(), file)
    
    update_log("        completed wst_real in: " + delta_time(start_wst) + " min", \
               log_name_now = log_name)
    
    ## ========= Pk calculus ==================================
    update_log("    beginning Pk",\
               log_name_now=log_name)
    start_pk = time.time()

    # create mesh
    mesh = binCat.to_mesh(resampler='tsc', Nmesh=N_mesh,
                          compensated=True,  # deconvolving
                          interlaced=True,   # antialiasing
                          position='Position', weight="Mass",
                          BoxSize=BoxSize
                          )
    r = FFTPower(mesh, mode='1d', dk=0.005, kmin=0.01)
    Pk = r.power
    with open('/home/jovyan/AA_Ricc/Results/Pk-files/fiducial_Pk_nbk_real.pk', 'ab') as file:
        pickle.dump(Pk, file)
    
    update_log("        completed Pk_real in: " + delta_time(start_pk) + " min",\
               log_name_now=log_name)

    print("    end evaluation in " + delta_time(strt) + "\n")
    
    
def CALCULUS(S, N_grid = 256, n_realiz = -1, N_mesh = 512,\
             Ff = 'fiducial', logger_name="a.log",
             root = '/home/jovyan/Data/Snapshots/',\
             sig = "s08", qu = "q08"
             ):
    print("in calculus")
    update_log("in CALCULUS", log_name_now=logger_name)
    if n_realiz > 0:
        num = n_realiz
        in_realizations = os.listdir(root+Ff)[0:num]
    elif n_realiz < 0:
        in_realizations = os.listdir(root+Ff)
        num = len(in_realizations)
    
    filename = Ff + '_coefficients_' + sig + '_' + qu + '_' + str(N_grid) + "_" + str(num) + '.wst'
    
    if not os.path.exists('/home/jovyan/AA_Ricc/Results/WST-files/'+filename):
      # os.remove('/home/riccardo/WST-files/'+filename)
      for i in range(len(in_realizations)):
            snapdir = root + Ff + '/' + in_realizations[i]
            HaloWST_one_f_MASL(S = S, filename = filename, snapdir = snapdir,\
                               N_grid = N_grid, N_mesh = N_mesh, i=i, log_name=logger_name)


# ==== MAIN ==============================================================================================

AAA = time.time()
# log info
now = datetime.now() + timedelta(hours=2)
log_name_now = str(now.strftime("%Y-%m-%d-(%H_%M_%S)") + ".log")
N_grid, N_mesh = 256, 512
N_realiz = 3
j, l = 4, 4
# dtype_cust = [("Position",    (np.float32, 3)),\
#               ("RSDPosition", (np.float32, 3)),\
#               ("Velocity",    (np.float32, 3)),\
#               ("Mass",         np.float32)]
dtype_cust = [("Position", (np.float32, 3)), ("Mass", np.float32)]

print("before HarmonicScattering")

log_name_begin = str(now.strftime("%Y/%m/%d - %H:%M:%S"))
update_log("START: " + log_name_begin, log_name_now=log_name_now)

if __name__=="__main__":
    S = HarmonicScattering3D(J=j, L=l, shape=(N_grid, N_grid, N_grid), sigma_0=0.8, integral_powers=[0.8])

    update_log("Completed `S` in: " + delta_time(AAA) +" min",\
            log_name_now=log_name_now)

    print("after HarmonicScattering")

    try:
        p1 = Process(target = CALCULUS,
                     args = (S, N_grid,
                             N_realiz, N_mesh,
                             'fiducial', log_name_now, ))
        p2 = Process(target = CALCULUS,
                     args = (S, N_grid,
                     N_realiz, N_mesh,
                     'h_m', log_name_now, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        # CALCULUS(S=S, N_grid=N_grid, n_realiz=N_realiz, N_mesh = N_mesh, Ff = 'fiducial', logger_name = log_name_now)
    except Exception as e:
        error_message = traceback.format_exc()
        with open('/home/jovyan/AA_Ricc/log/'+log_name_now, 'a') as f:
            f.write("\n\n\nERROR >.<\n\n" + error_message)

end = datetime.now() + timedelta(hours=2)
log_name_end = str(end.strftime("%Y/%m/%d - %H:%M:%S"))
update_log("\nEND date: " + log_name_end,\
           log_name_now=log_name_now)