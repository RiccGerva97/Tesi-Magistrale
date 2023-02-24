import numpy as np

# calc covariance matrix inverce using Hartlap correction factor
def Hartlap(mat, Nr = 350):
    """Calculates inverse matrix using Hartlap correction.
    Arguments:
    - `mat`: input matrix to invert
    - `Nr`: nuber of realization used o calculated the matrix
    """
    return (Nr-len(mat)-2)/(Nr-1)*np.linalg(mat)

# calc Jacobian matrix of WST coeff. over cosmological parameters
def JacobCosmPar(WSTc_0, WSTc_1, ComsP_0, CosmP_1):
    """Returns the Jacobian matrix of WST coefficients. Uses incremental ratio
    between WST coeff and cosmological parameters of two different cosmologies.
    """
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

# calculates Fisher matrix
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

