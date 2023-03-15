import sys
import getopt

import sys
sys.path.insert(1, './MyFunc')
from CalcWST import CALCULUS
from myDict import boolean

def line_parser(argv):
    """Function that parses the inputs given from command line when executing
    `calc_WST_halos.py`
    """
    try:
        opts, args = getopt.getopt(argv,"hvo:g:w:r:F:",["onefiles=","gridcells=","wstcells=","realization=","folders="])
    except getopt.GetoptError:
        print ('calc_WST_halo.py -o <one outfile> -g <cell density grid> -w <cell WST coeff> -r <realizations> -F <folder1 folder2 ...> -v <verbose opt>')
        sys.exit(2)

    if len(opts) == 0:
        return CALCULUS() # giusto?
        
    N_hgrid, N_WSTgrid, n_realiz= '256', '256', '-1'
    togheter = "True"
    folders = ['fiducial']
    
    for opt, arg in opts:
        if opt in '-h':
            print ('calc_WST_halo.py -o <one outfile> -g <cell density grid> -w <cell WST coeff> -r <realizations> -F <folder1 folder2 ...>//<ALL> -v <verbose opt>')
            sys.exit()
        # è giusto questo if o serve un altro "operatore logico"?
        if opt in ("-v", "--verbose"):
            togheter = bool(boolean[input("Write results on one file? [TRUE/False] ") or "True"])
            N_hgrid = int(input("Number of cells per side of density matrix [256]: ") or "256")
            N_WSTgrid = int(input("Number of cells per side of WST coefficients evaluation [256]: ") or "256")
            n_realiz = int(input("Number of realizations to use ['Enter' for all]: ") or "-1")
            f = input("Cosmologies to evaluate WST coefficients (separate with ' ') [ALL]: ") or "ALL"
            if f == "ALL":
                folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp', \
                    'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', 'Om_m', 'Om_p', \
                        's8_m', 's8_p', 'w_m', 'w_p']
            else:
                folders = f.split()
        elif opt in ("-o", "--onefiles"):
            togheter = bool(boolean[arg])
        elif opt in ("-g", "--gridcells"):
            N_hgrid = arg
        elif opt in ("-w", "--wstcells"):
            N_WSTgrid = arg
        elif opt in ("-r", "--realization"):
            n_realiz = arg
        elif opt in ("-F", "--folders"):
            if arg == "ALL":
                folders = ['fiducial', 'h_m', 'h_p', 'Mnu_p', 'Mnu_pp' ,'Mnu_ppp',\
                     'ns_m', 'ns_p', 'Ob_m', 'Ob_p', 'Ob2_m', 'Ob2_p', \
                        'Om_m', 'Om_p', 's8_m', 's8_p', 'w_m', 'w_p']
            else:
                folders = arg.split()
    
    return CALCULUS(togheter, int(N_hgrid), int(N_WSTgrid), int(n_realiz), folders)