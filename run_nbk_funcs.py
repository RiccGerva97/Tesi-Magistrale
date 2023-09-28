import numpy as np

def info_name(name):
    """Obtain realization information from namefile"""
    # assert type(name) == str
    print("TYPE: ", type(name))
    # info = name.split('_')
    info = name.split('_')[-3:]
    print("TYPE: ", info, "\n", type(info))
    info[2] = info[2].replace(".wst", "")
    N_hgrid = info[0]
    N_WSTgrid = info[1]
    n_realiz = info[2].replace(".wst", "")  
    return [int(N_hgrid), int(N_WSTgrid), int(n_realiz)]

def cosmo_parser(name):
    """Obtain cosmology from .wst file"""
    info = name.split('_')
    if info[0] == "fiducial":
        return info[0]
    elif info[0] == "zeldovich":
        return info[0]
    else:
        return info[0] + "_" + info[1]
    
def PacMan(x, d = np.array((0, 0, 1000)) ):
    """Returns a number x in the interval [0; d]"""
    if 0 <= x[2] <= d[2]:
        return x
    elif x[2] > d[2]:
        return PacMan(x - d)
    elif x[2] < 0:
        return PacMan(x + d)

def Hartlap(mat, Nr = 350):
    """Calculates inverse matrix using Hartlap correction.
    Arguments:
    - `mat`: input matrix to invert
    - `Nr`: nuber of realization used o calculated the matrix
    """
    return (Nr-len(mat)-2)/(Nr-1)*np.linalg.inv(mat)

def error_message():
        print("     ___________")
        print("    /           \\ ")
        print("== ( ERROR >.<   ) ==")
        print("    \\___________/ ")
