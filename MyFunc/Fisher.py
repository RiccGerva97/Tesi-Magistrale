import numpy as np

# calc covariance matrix inverce using Hartlap correction factor
def Hartlap(mat, Nr = 350):
    return (Nr-len(mat)-2)/(Nr-1)*np.linalg(mat)

# calc Jacobian matrix of WST coeff. over cosmological parameters
def JacobCosmPar(WSTc_0, WSTc_1, ComsP_0, CosmP_1):
    m = len(WSTc_0)
    alpha = len(ComsP_0)
    Jac = np.zeros((m, alpha))
    for i in range(m):
        for j in range(alpha):
            Jac[i][j] = (WSTc_1[i]-WSTc_0[i])/(CosmP_1[j]-ComsP_0[j])
    return Jac

# calculates Fisher matrix
def Fisher(WSTc_0, WSTc_1, ComsP_0, CosmP_1, Nr = 350):
    C = Hartlap(WSTc_0, Nr)
    D = JacobCosmPar(WSTc_0, WSTc_1, ComsP_0, CosmP_1)
    return np.matmul(D, np.matmul(C, D))

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

