import numpy as np
from MyFunc.myDict import order_folders, COSMOPAR

def correlation_matrix(m):
    """Calculates the correlation matrix of matrix m_ij.
    Tests if it's 75x75
    """
    avg = np.average(m, axis=0)
    dim = len(avg)
    # assert dim == 75
    # realiz = len(m[0])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # VARIATION
    sigma = []
    for i in range(dim):
        sigma.append(np.sum((avg[i] - m[i])**2))
    sigma = np.sqrt(sigma)
    
    sigma_bis = []
    for i in range(dim):
        cum = 0
        for j in range(len(m[i])):
            cum += (avg[i] - m[i][j])**2
        sigma_bis.append(cum)
    sigma_bis = np.sqrt(sigma_bis)
    # print("sigma:", np.shape(sigma), "\n", sigma)
    # print("\nsigma_bis:", np.shape(sigma_bis), "\n", sigma_bis)
    # print("\nDIFFERENCE:\n", np.where(np.abs(sigma - sigma_bis)>1e-2))
    # assert not abs(sigma - sigma_bis).all() > 1e-2, "¶ ERROR: inconsistence in evaluating variance"
            
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # # COVARIANCE MATRIX
    # c = np.zeros((dim, dim))
    # for i in range(dim):
    #     for j in range(dim):
    #         c[i, j] = np.sum((avg[i] - m[i])*(avg[j] - m[j]))
    # assert np.shape(c) == (75, 75)

    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # # CORRELATION MATRIX
    # CORR = np.zeros((dim, dim))
    # for i in range(dim):
    #     for j in range(dim):
    #         CORR[i, j] = c[i, j] / (sigma[i] * sigma[j])

    # SHORTER WAY
    #
    CORR = np.zeros((dim, dim))

    for i in range(dim):
        for j in range(dim):
            cum = 0
            for k in range(len(m[i])):
                cum += (avg[i] - m[i][k])*(avg[j] - m[j][k])
            CORR[i, j] = cum  / (sigma_bis[i] * sigma_bis[j])


    # for i in range(dim):
    #     for j in range(dim):
    #         CORR[i, j] = np.sum((avg[i] - m[i])*(avg[j] - m[j])) / (sigma_bis[i] * sigma_bis[j])
    # #
    # assert np.shape(CORR) == (75, 75), "ERROR in evaluating correlation matrix"
    if np.linalg.det(CORR) == 0:
        print("¶ WARNING: correlation matrix is singular")
    
    return CORR

def Hartlap(mat, Nr = 350):
    """Calculates inverse matrix using Hartlap correction.
    Arguments:
    - `mat`: input matrix to invert
    - `Nr`: nuber of realization used o calculated the matrix
    """
    return (Nr-len(mat)-2)/(Nr-1)*np.linalg.inv(mat)

def JacobCosmPar(WSTc_0, WSTc_1, ComsP_0, CosmP_1):
    """Returns the Jacobian matrix of WST coefficients. Uses incremental ratio
    between WST coeff and cosmological parameters of two different cosmologies.
    """
    # here I give as input WST coeffs of a cosmology
    m = len(WSTc_0)         # observables lenght
    alpha = len(ComsP_0)    # parameters lenght
    Jac = np.zeros((m, alpha))
    for i in range(m):
        for j in range(alpha):
            if np.abs(CosmP_1[j] - ComsP_0[j]) < 1e-10:
                Jac[i][j] = (WSTc_1[i]-WSTc_0[i]) / (CosmP_1[j]-ComsP_0[j])
            else:
                Jac[i][j] = 0
    return Jac


def Fisher(WSTc_0, WSTc_1, ComsP_0, CosmP_1, Nr = 350):
    """Calculates Fisher matrix of cosmological parameters 
    """
    C = Hartlap(WSTc_0, Nr)
    D = JacobCosmPar(WSTc_0, WSTc_1, ComsP_0, CosmP_1)
    return np.matmul(D, np.matmul(C, D))

def MatFisher(H, J, Nr = 350):
    """Calculates Fischer matrix giving:
    - Hartlap matrix
    - Jacobian of observables
    """
    F = np.zeros((len(J[0]), len(J[0])))
    for alpha in range(len(J[:0])):
        for betha in range(len(J[:0])):
            for i in range(len(J[0])):
                for j in range(len(J[0])):
                    F[alpha][betha] += J[alpha][i] * H[i][j] * J[betha][j]


    return


# calculates cosmological parameters error inferior boundary
def Sigma(mat):
    M = np.diag(mat)
    theta = []
    for i in range(len(M)):
        theta.append(M[i])
    return np.sqrt(np.linalg(theta))

    # dim = len(WSTc_0)
    # for i in range(dim):
    #     for j in range(dim):
    #         F[i][j] = Sum(D[:i], C, D[:j])


class CovM:
    def __init__(self, WSTc_0, WSTc_1, ComsP_0, CosmP_1, Nr = 350):
        self.InvMat = Fisher(WSTc_0, WSTc_1, ComsP_0, CosmP_1, Nr = 350)
        self.DiagIM = np.diag(self.InvMat)