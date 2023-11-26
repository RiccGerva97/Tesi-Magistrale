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
    
def PacMan(x, d = np.array((0, 0, 1000.)) ):
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

def HubblePar( z, O_m, H_0 = 67.11, O_k = 0, O_de = -1, w = -1):
    """Evaluates the Hubble parameter depending on redshift `z` and cosmological parameters."""
    if H_0 < 1.: H_0 *= 100.
    if O_de == -1: O_de = 1 - (O_m + O_k)
    # print(z, " ", O_m, " ", H_0, " ", O_de, " ", O_de* (1+z)**(3*(1+w)))
    A = H_0**2 * (O_m * (1+z)**3 +\
                  O_k * (1+z)**2 +\
                  O_de* (1+z)**(3*(1+w))  )
    return np.sqrt(A)


def covariation_matrix(m):
    """Calculates the correlation matrix of matrix m_ij.
    """
    avg = np.average(m, axis=0)    # mean values
    dim = len(avg)                 # number of variables
    N = len(m[0])                  # number of values per varaible

    COV = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            cum = 0.
            for k in range(len(m[i])):
                cum += (avg[i] - m[i][k])*(avg[j] - m[j][k])
            COV[i, j] = cum/N

    if np.linalg.det(COV) == 0:
        print("¶ WARNING: correlation matrix is singular")
    
    return np.sqrt(COV)

def error_message(a = "ERROR >.<"):
    N = len(a)
    print("")
    print(" "*6 + "_"*N)
    print(" "*5+"/" + " "*N + "\\")
    print(" === | " + a + "| ===")
    print(" "*5 + "\\" + "_"*N + "/" )
    print("")