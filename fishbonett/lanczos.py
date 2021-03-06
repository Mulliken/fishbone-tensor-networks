"""
    Tridiagonalization function by the Lanczos iterations.
    The following code is excerpted from
    https://github.com/matenure/FastGCN/blob/master/lanczos.py
    The algorithm is closely following the algorithm 10.3 and 10.4 in
    http://people.inf.ethz.ch/arbenz/ewp/Lnotes/chapter10.pdf
"""
import numpy as np
from math import fsum

def lanczos(A,p):
    q = np.array(p).copy()
    n = k = A.shape[0]
    Q = np.zeros((n,k+1))
    Q[:,0] = q/np.linalg.norm(q)
    # print(Q[:,0])
    alpha = 0
    beta = 0

    for i in range(k):
      if i == 0:
        q = np.dot(A,Q[:,i])
      else:
        q = np.dot(A, Q[:,i]) - beta*Q[:,i-1]
      alpha = np.dot(q.T, Q[:,i])
      q = q - Q[:,i]*alpha
      q = q - np.dot(Q[:,:i], np.dot(Q[:,:i].T, q)) # full reorthogonalization
      beta = np.linalg.norm(q)
      Q[:,i+1] = q/beta
      # print(beta)

    Q = Q[:,:k]

    Sigma = np.dot(Q.T, np.dot(A, Q))
    return Sigma, Q


if __name__ == "__main__":
    dim = 1000
    ele = np.random.rand(dim)*1000
    ele.sort()
    mat = np.diag(ele)
    v0 = np.random.rand(dim)*1
    T, Q = lanczos(mat, v0)
    print(np.sort(np.linalg.eigvals(T)) - ele
          )
    print(Q.T@Q-np.eye(Q.shape[0]))

