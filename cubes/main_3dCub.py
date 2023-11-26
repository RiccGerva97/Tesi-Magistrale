import sys, time, os, pickle, traceback
import h5py#, hdf5plugin
import kymatio, readgadget, nbodykit

import globus_sdk                                     # <<< decomment!
from globus_sdk import \
    TransferScopes, ConfidentialAppAuthClient, TransferClient

import numpy as np

from kymatio.torch import HarmonicScattering3D
from readfof import FoF_catalog
from torch import flatten, from_numpy
from datetime import datetime, timedelta
from shutil import rmtree

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

cosmologies = {
    0   : 'fiducial'  ,
    1   : 'h_m'       ,
    2   : 'h_p'       ,
    3   : 'Mnu_p'     ,
    4   : 'Mnu_pp'    ,
    5   : 'Mnu_ppp'   ,
    6   : 'ns_m'      ,
    7   : 'ns_p'      ,
    8   : 'Ob2_m'     ,
    9   : 'Ob2_p'     ,
    10  : 'Om_m'      ,
    11  : 'Om_p'      ,
    12  : 's8_m'      ,
    13  : 's8_p'      ,
    14  : 'w_m'       ,
    15  : 'w_p'       ,
    16  : 'zeldovich' 
}

# ==== FUNCTIONS =====================================================================

def cosmo_parser(name):
    """Obtain cosmology from .wst file"""
    info = name.split('_')
    if info[0] == "fiducial": return info[0]
    elif info[0] == "zeldovich": return info[0]
    else: return info[0] + "_" + info[1]

def delta_time(T):
    return str(round((time.time()-T)/60, 3))

def update_log(a, log_name_now):
    if not type(a) == str: a = str(a) 
    # with open('/home/riccardo/SUBMIT/log_prints/'+log_name_now, 'a') as f: f.write("\n"+a)
    with open('/home/AA_Ricc/log/'+log_name_now, 'a') as f: f.write("\n"+a)

def HaloWST_one_f_MASL(
        S, filename, snapdir, i,
        snapnum=2, N_grid=256, N_mesh=512,
        hlength=1000, j=4, l=4,
        log_name="a.log",
    ):

    cosmo = cosmo_parser(filename)

    # real begin
    strt = time.time()
    print("in evaluation")
    update_log(
        "  "+cosmo+" in evaluation",
        log_name_now=log_name
    )
    # initialize folder indications
    snapshot = snapdir + '/df_m_256_CIC_z=0.npy'
    density = np.load(snapshot)
    
    ## ========= WST claulus ===================================================================================================
    update_log(
        "    "+cosmo+": beginning WST",\
        log_name_now=log_name
    )
    start_wst = time.time()

    Sx = S.scattering(from_numpy(density))
    # with open('/home/riccardo/WST_snap_files/' +
    with open('/home/AA_Ricc/Results/WST-files/' +
            #   filename.replace("_coefficients_", "_coefficients_M_real_"), 'ab') as file:
            filename, 'ab') as file:
        pickle.dump(flatten(Sx, start_dim=0).cpu().detach().numpy(), file)
    
    update_log("        completed wst_real in: " + delta_time(start_wst) + " min", \
               log_name_now = log_name)
    
    ## ========= Pk calculus ====================================================================================================
    update_log(
        "    "+cosmo+": beginning Pk",
        log_name_now=log_name
    )
    start_pk = time.time()

    r = FFTPower(density, mode='1d', dk=0.005, kmin=0.01)
    Pk = r.power
    # with open('/home/riccardo/Pk_snap_files/'
    with open('/home/AA_Ricc/Results/Pk-files/' +
              +filename.replace('.wst', '.pk'), 'ab') as file:
        pickle.dump(Pk, file)
    
    update_log(
        "    "+cosmo+": completed Pk_real in: " + delta_time(start_pk) + " min",
        log_name_now=log_name
    )
    update_log(
        "    "+cosmo+": end evaluation in " + delta_time(strt) + "\n",
        log_name_now=log_name
    )
    print("    "+cosmo+": end evaluation in " + delta_time(strt) + "\n")
    
    
def CALCULUS(S, N_grid = 256, n_realiz = -1, N_mesh = 512,\
             Ff = 'fiducial', logger_name="a.log",
             root = '/home/jovyan/Data/Snapshots/',\
             sig = "s08", qu = "q08"
             ):
    print(Ff+": in calculus")
    update_log("in CALCULUS", log_name_now=logger_name)
    
    if n_realiz > 0:
        num = n_realiz
        in_realizations = os.listdir(root+Ff)[0:num]
    elif n_realiz < 0:
        in_realizations = os.listdir(root+Ff)
        num = len(in_realizations)
    
    # filename = Ff + '_coefficients_' + sig + '_' + qu + '_' + str(N_grid) + "_" + str(num) + '.wst'
    filename = Ff + '_coefficients_real.wst'
    
    if not os.path.exists('/home/riccardo/WST-3D-files/'+filename):
      # os.remove('/home/riccardo/WST-files/'+filename)
        for i in range(len(in_realizations)):
            snapdir = root + Ff + '/' + in_realizations[i]
            HaloWST_one_f_MASL(
                S = S,
                filename = filename,
                snapdir = snapdir,
                N_grid = N_grid,
                N_mesh = N_mesh,
                i = i,
                log_name = logger_name
            )


# ==== MAIN ==============================================================================================

AAA = time.time()

# log info
now = datetime.now() + timedelta(hours=2)
log_name_now = str(now.strftime("%Y-%m-%d-(%H_%M_%S)") + ".log")
N_grid, N_mesh = 256, 512
N_mesh = 256
N_realiz = -1
j, l = 4, 4
# dtype_cust = [
#     ("Position",    (np.float32, 3)),
#     ("RSDPosition", (np.float32, 3)),
#     ("Velocity",    (np.float32, 3)),
#     ("Mass",         np.float32)
# ]
dtype_cust = [
    ("Position", (np.float32, 3)),
    ("Mass", np.float32)
]

root_Q = "~/Snapshots/"
root_D = "/workplace/riccardo/3D_cubes/"
root_D_log = "/home/riccardo/SUBMIT/log_prints/"

# MAIN
if __name__=="__main__":
    n = int(sys.argv[1])
    cosmo = cosmologies[n]

    # Create log file
    log_name_begin = cosmo + str(now.strftime("%Y/%m/%d - %H:%M:%S"))
    # with open('/home/riccardo/SUBMIT/log_prints/'+log_name_now, 'a') as f:
    with open(root_D_log+log_name_now, 'a') as f:
        f.write("START: " + log_name_begin + "\n")
    print(log_name_begin)

    # if cosmo == "fiducial": N_realiz = 1000
    # elif "ZA" in cosmo: N_realiz = 500
    # else: N_realiz = 350

    root_Q += cosmo+"/"
    root_D += cosmo+"/"

    S = HarmonicScattering3D(J=j, L=l, shape=(N_grid, N_grid, N_grid), sigma_0=0.8, integral_powers=[0.8])

    update_log(
        "Completed `S` in: " + delta_time(AAA) +" min",\
        log_name_now=log_name_now
    )
    print("after HarmonicScattering")

    try:
        CALCULUS(
            S=S,
            N_grid=N_grid, n_realiz=N_realiz, N_mesh = N_mesh,
            Ff = cosmo,
            root = root_D,
            logger_name = log_name_now
            )
    except Exception as e:
        error_message = traceback.format_exc()
        # with open('/home/jovyan/AA_Ricc/log/'+log_name_now, 'a') as f:
        with open('/home/riccardo/SUBMIT/log/'+log_name_now, 'a') as f:
            f.write("\n\n\nERROR >.<\n\n" + error_message)

# end log
end = datetime.now() + timedelta(hours=2)
log_name_end = str(end.strftime("%Y/%m/%d - %H:%M:%S"))
update_log("\nEND date: " + log_name_end,\
           log_name_now=log_name_now)