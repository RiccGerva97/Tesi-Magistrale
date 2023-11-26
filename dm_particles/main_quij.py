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

endpoints = {
    "3D_density_Quijote" : "bbcfa486-90ec-11ed-959b-63a4785a3eec",
    "DebianServer"       : "abf51c76-7723-11ee-b166-7d6eafac2be9",
    "DoraemonRicc"       : "9545d8ac-74d6-11ee-b164-7d6eafac2be9",
    "HDD1disk"           : "9eb93f5a-6c2a-11ee-ad2b-9197a4554f81",
    "VolD"               : "40f0f796-70d5-11ee-b162-7d6eafac2be9",
    "Quijote_NY"         : "e0eae0aa-5bca-11ea-9683-0e56c063f437"
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
    # check download of the current folder is completed
    with open(f'./{cosmo}_taskID.txt', 'r') as f:
        task_id_old = f.read()
    w_bool = True
    while w_bool:
        task = transfer_client.get_task(task_id_old)
        # w_bool = not task["status"] == "SUCCEEDED"
        if task["status"] == "SUCCEEDED": w_bool = True
        elif task["status"] == "FAILED": 
            print("Transfer task failed.", flush=True)
            break
        elif task["status"] in ["ACTIVE", "INACTIVE"]: print("")
        else: assert False, "Problem in task status"
        time.sleep(5)

    # real begin
    strt = time.time()
    print("in evaluation")
    update_log(
        "  "+cosmo+" in evaluation",
        log_name_now=log_name
    )
    # initialize folder indications
    snapshot = snapdir + '/snapdir_000/snap_000'
    ptype    = [1]

    # ==== read datas and cosmologiy's info ====================================================================================
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


    # >>>> manage snapshots files >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # delete already readed files
    fold = os.listdir(f'{root_D}{cosmo}/')
    assert len(fold) == 1, f">.< | Error in snapshots {cosmo} storage | >.<"
    rmtree(f'{root_D}{cosmo}/{fold[0]}')
    task_data = globus_sdk.TransferData(
        source_endpoint=source_endpoint_id,
        destination_endpoint=dest_endpoint_id
    )
    task_data.add_item(
        f"{root_Q}{cosmo}/{int(fold[0])+1}/snapdir_000/",
        f"{root_D}{cosmo}/{int(fold[0])+1}/snapdir_000/",
        recursive=True,
    )
    task_doc = transfer_client.submit_transfer(task_data)
    task_id = task_doc["task_id"]
    # write task id on file for check if
    # download is completed on the next folder
    with open(f'./{cosmo}_taskID.txt', 'w') as f:
        f.write(task_id)
    update_log(
        f"submitted transfer, task_id={task_id}",
        log_name_now=log_name_now
    )
    # <<<< manage snapshots files <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    with open('./data_source.dat', "wb") as ff:
        # pos_h.tofile(ff); pos_rsd.tofile(ff); vel.tofile(ff); mass.tofile(ff)
        pos.tofile(ff); np.full(len(pos), Masses[1], dtype=np.float32).tofile(ff)
        ff.seek(0)
    
    # create catalog obj
    binCat = BinaryCatalog(ff.name, dtype_cust)

    ## ========= WST claulus ===================================================================================================
    update_log(
        "    "+cosmo+": beginning WST",\
        log_name_now=log_name
    )
    start_wst = time.time()

    mesh_wst = binCat.to_mesh(
        resampler='cic', Nmesh=N_grid,
        compensated=True,  # deconvolving
        interlaced=True,   # antialiasing
        position='Position', weight="Mass",
        BoxSize=BoxSize
    )
    # initialize density
    dens = mesh_wst.preview().astype('float32')

    update_log("    "+cosmo+": finished MASL.MA", log_name_now=log_name)

    Sx = S.scattering(from_numpy(dens))
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

    # create mesh
    mesh = binCat.to_mesh(
        resampler='cic', Nmesh=N_mesh,
        compensated=True,  # deconvolving
        interlaced=True,   # antialiasing
        position='Position', weight="Mass",
        BoxSize=BoxSize
    )
    r = FFTPower(mesh, mode='1d', dk=0.005, kmin=0.01)
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
    
    if not os.path.exists('/home/jovyan/AA_Ricc/Results/WST-files/'+filename):
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
N_realiz = 100
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
root_D = "/workplace/riccardo/Snapshots/"
root_D_log = "/home/riccardo/SUBMIT/log_prints"

# Globus initialization
CLIENT_ID = '8cbf76f8-04e7-4d6e-ab59-2e60b182ec83'
CLIENT_SECRET = 'BVaTBYLMQn7BeSfZDM/dCJANRGDi/cUMKqTwEh134hY='
auth_client = ConfidentialAppAuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    app_name="Tesi3",
)
tokens = auth_client.oauth2_client_credentials_tokens()
access_token = tokens.by_resource_server["transfer.api.globus.org"]["access_token"]
transfer_client = TransferClient(authorizer=globus_sdk.AccessTokenAuthorizer(access_token))

source_endpoint_id = endpoints["Quijote_NY"]
dest_endpoint_id = endpoints["VolD"]


# Create log file
log_name_begin = str(now.strftime("%Y/%m/%d - %H:%M:%S"))
with open('/home/riccardo/SUBMIT/log_prints/'+log_name_now, 'a') as f:
    f.write("START: " + log_name_begin + "\n")
print(log_name_begin)

# MAIN
if __name__=="__main__":
    cosmo = sys.argv[1]
    if not type(cosmo) == str: cosmo=str(cosmo)

    root_Q += cosmo+"/"
    root_D += cosmo+"/"

    task_data = globus_sdk.TransferData(
        source_endpoint=source_endpoint_id,
        destination_endpoint=dest_endpoint_id
    )

    task_data.add_item(
        root_Q + "/0/snapdir_000/",
        root_D + "/0/snapdir_000/",
        recursive=True
    )
    task_doc = transfer_client.submit_transfer(task_data)
    task_id = task_doc["task_id"]
    with open(f'./{cosmo}_taskID.txt', 'w') as f:
        f.write(task_id)
    update_log(
        f"submitted transfer, task_id={task_id}",
        log_name_now=log_name_now
    )

    S = HarmonicScattering3D(J=j, L=l, shape=(N_grid, N_grid, N_grid), sigma_0=0.8, integral_powers=[0.8])

    update_log(
        "Completed `S` in: " + delta_time(AAA) +" min",\
        log_name_now=log_name_now
    )
    print("after HarmonicScattering")

    try:
        CALCULUS(S=S, N_grid=N_grid, n_realiz=N_realiz, N_mesh = N_mesh, Ff = cosmo, logger_name = log_name_now)
    except Exception as e:
        error_message = traceback.format_exc()
        with open('/home/jovyan/AA_Ricc/log/'+log_name_now, 'a') as f:
            f.write("\n\n\nERROR >.<\n\n" + error_message)

# end log
end = datetime.now() + timedelta(hours=2)
log_name_end = str(end.strftime("%Y/%m/%d - %H:%M:%S"))
update_log("\nEND date: " + log_name_end,\
           log_name_now=log_name_now)