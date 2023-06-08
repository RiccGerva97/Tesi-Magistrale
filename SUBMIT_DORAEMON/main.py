import os
import sys
sys.path.insert(1, './MyFunc')
from MyFunc.name_parser import info_name, cosmo_parser
from MyFunc.WST_eval import CALCULUS

# READ list file to use SLURM_ARRAY_TASK_ID
lines = []
with open("file_list_to_create.txt", 'rb') as file:
    lines = file.readlines()

# SAVES parameters, assuming all cosmologies are calculated with same parameters
info = info_name(lines[0].decode("utf-8"))
N_hgrid = info[0]
N_WSTgrid = info[1]

# SAVES cosmology names
name_list = []
for i in range(len(lines)):
    name_list.append(cosmo_parser(lines[i].decode("utf-8")))

if __name__ == "__main__":
    n = sys.argv[1]
    n = int(n)
    if name_list[n] == "fiducial":
        n_realiz = 1000
    elif name_list[n] == "zeldovich":
        n_realiz = 500
    else:
        n_realiz = info[2]
    
    # REMEMBER TO REMOVE!!!
    n_realiz = 1
    
    CALCULUS(N_hgrid=N_hgrid, N_WSTgrid=N_WSTgrid, n_realiz=n_realiz, Ff = [name_list[n]])