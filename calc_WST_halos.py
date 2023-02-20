import sys
import getopt
sys.path.insert(1, './MyFunc')
from CalcWST import HaloWST_f

import os
import pickle

def CALCULUS(N_hgrid = 128, N_WSTgrid = 128, n_realiz = 350, Ff = ['fiducial']):
    
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
    Fif = '_first_order_'+str(N_hgrid)+"_"+str(N_hgrid)+"_"+str(N_hgrid)+'.wst'
    Sef = '_second_order_'+str(N_hgrid)+"_"+str(N_hgrid)+"_"+str(N_hgrid)+'.wst'


    # define root path where to find hale catalogues
    root = '/media/fuffolo97/HDD1/UNI/Tesi/Halos/FoF/'

    # choose cosmologies 
    folders = Ff

    # loop over cosmologies, calculate and create file WST coeff
    for folder in tqdm(folders):

        # delete existing file, want a new one (not extending it)
        if os.path.exists(folder+Fif):
            os.remove(folder+Fif)
        if os.path.exists(folder+Sef):
            os.remove(folder+Sef)
        
        # loop over the different realizations
        for i in tqdm(range(n_realiz), leave=False):
            snapdir = root + folder +'/%d'%i
            HaloWST_f(folder+Fif, folder+Sef, snapdir, N_hgrid = N_hgrid, N_WSTgrid = N_WSTgrid)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hvg:w:r:F:",["gridcells=","wstcells=","realization=","folders="])
    except getopt.GetoptError:
        print ('calc_WST_halo.py -g <cell density grid> -w <cell WST coeff> -r <realizations> -F <folder1 folder2 ...> -v <verbose opt>')
        sys.exit(2)

    if len(opts) == 0:
        CALCULUS()
        
    N_hgrid, N_WSTgrid, n_realiz= '128', '128', '1'
    folders = ['fiducial']
    
    for opt, arg in opts:
        if opt in '-h':
            print ('calc_WST_halo.py -g <cell density grid> -w <cell WST coeff> -r <realizations> -F <folder1 folder2 ...>//<ALL> -v <verbose opt>')
            sys.exit()
        elif opt in ("-v", "--verbose"):
            print("Number of cells per side of density matrix [128]:")
            N_hgrid = int(input() or "128")
            print("Number of cells per side of WST coefficients evaluation  [128]:")
            N_WSTgrid = int(input() or "128")
            print("Number of cells per side of WST coefficients evaluation  [350]:")
            n_realiz = int(input() or "350")
            print("Cosmologies to evaluate WST coefficients (separated by space, type ALL for all cosmologies):")
            f = input() or "fiducial"
            if f == "ALL":
                folders = ['EQ_m', 'EQ_p', 'fiducial', 'LC_m', 'LC_m50', 'LC_p', 'LC_p50', 'OR_CMB_m', 'OR_CMB_p', 'OR_LSS_m', 'OR_LSS_p']
            else:
                folders = f.split()
        elif opt in ("-g", "--gridcells"):
            N_hgrid = arg
        elif opt in ("-w", "--wstcells"):
            N_WSTgrid = arg
        elif opt in ("-r", "--realization"):
            n_realiz = arg
        elif opt in ("-F", "--folders"):
            if arg == "ALL":
                folders = ['EQ_m', 'EQ_p', 'fiducial', 'LC_m', 'LC_m50', 'LC_p', 'LC_p50', 'OR_CMB_m', 'OR_CMB_p', 'OR_LSS_m', 'OR_LSS_p']
            else:
                folders = arg.split()
    
    CALCULUS(int(N_hgrid), int(N_WSTgrid), int(n_realiz), folders)

if __name__ == "__main__":
   main(sys.argv[1:])

# first_order_coeffs = []
# second_order_coeffs = []

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