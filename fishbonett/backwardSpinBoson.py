import numpy as np

from scipy.linalg import svd as csvd
from fbpca import pca as rsvd
from opt_einsum import contract as einsum
from scipy.sparse.linalg import expm as sparseExpm
from scipy.sparse import csc_matrix
from numpy import exp
import fishbonett.recurrence_coefficients as rc
from copy import deepcopy as dcopy
from scipy.sparse import kron as skron
import scipy.integrate as integrate

def _c(dim: int):
    """
    Creates the annihilation operator.
    This fuction is from the package py-tedopa/tedopa.
    https://github.com/MoritzLange/py-tedopa/tedopa/

    The BSD 3-Clause License
    Copyright (c) 2018, the py-tedopa developers.
    All rights reserved.

    :param dim: Dimension of the site it should act on
    :type dim: int
    :return: The annihilation operator
    :rtype: numpy.ndarray
    """
    op = np.zeros((dim, dim))
    for i in range(dim - 1):
        op[i, i + 1] = np.sqrt(i + 1)
    return op


def eye(d):
    if d == [] or None:
        return None
    elif type(d) is int or d is str:
        return np.eye(int(d))
    elif type(d) is list or np.ndarray:
        return np.eye(*d)


def kron(a, b):
    if a is None or b is None:
        return None
    if type(a) is list and type(b) is list:
        return skron(*a, *b, format='csc')
    if type(a) is list and type(b) is not list:
        return skron(*a, b, format='csc')
    if type(a) is not list and type(b) is list:
        return skron(a, *b, format='csc')
    else:
        return skron(a, b, format='csc')


def svd(A, b, full_matrices=False):
    dim = min(A.shape[0], A.shape[1])
    b = min(b, dim)
    if b >= 0:
        # print("CSVD", A.shape, b)
        # cs = csvd(A, full_matrices=False)
        print("RRSVD", A.shape, b)
        rs = rsvd(A, b, True, n_iter=2, l=2 * b)
        # print("Difference", diffsnorm(A, *B))
        # print(cs[1] - rs[1])
        return rs
    else:
        return csvd(A, full_matrices=False)


def calc_U(H, dt):
    """Given the H_bonds, calculate ``U_bonds[i] = expm(-dt*H_bonds[i])``.

    Each local operator has legs (i out, (i+1) out, i in, (i+1) in), in short ``i j i* j*``.
    Note that no imaginary 'i' is included, thus real `dt` means 'imaginary time' evolution!
    """
    H_sparse = csc_matrix(H)
    return sparseExpm(-dt * 1j * H_sparse)


def _to_list(x):
    """
    Converts x to [x] if x is a np.ndarray. If x is None,
    convert x(=None) to []. If x is already a list of a
    np.ndarray return x itself. Else if x is not a list of
    just one np.ndarray, raise TypeError.
    :param x: an np.array or a list of one np.ndarray
    :type x:
    :return:
    :rtype:
    """
    if x is None:
        return []
    elif x is list:
        return x
    else:
        return [x]


class SpinBoson1D:

    def __init__(self, pd):
        def g_state(dim):
            tensor = np.zeros(dim)
            tensor[(0,) * len(dim)] = 1.
            return tensor

        self.pd_spin = pd[-1]
        self.pd_boson = pd[0:-1]
        self.B = [g_state([1, d, 1]) for d in pd]
        self.S = [np.ones([1], np.float) for d in pd]
        self.U = [np.zeros(0) for d in pd[1:]]

    def get_theta1(self, i: int):
        return np.tensordot(np.diag(self.S[i]), self.B[i], [1, 0])

    def get_theta2(self, i: int):
        j = (i + 1)
        return np.tensordot(self.get_theta1(i), self.B[j], [2, 0])

    def split_truncate_theta(self, theta, i: int, chi_max: int, eps: float):
        (chi_left_on_left, phys_left,
         phys_right, chi_right_on_right) = theta.shape
        theta = np.reshape(theta, [chi_left_on_left * phys_left,
                                   phys_right * chi_right_on_right])
        A, S, B = svd(theta, chi_max, full_matrices=False)
        chivC = min(chi_max, np.sum(S > eps))
        print("Error Is", np.sum(S > eps), chi_max, S[chivC:] @ S[chivC:], chivC)
        # keep the largest `chivC` singular values
        piv = np.argsort(S)[::-1][:chivC]
        A, S, B = A[:, piv], S[piv], B[piv, :]
        S = S / np.linalg.norm(S)
        # A: {vL*i, chivC} -> vL i vR=chivC
        A = np.reshape(A, [chi_left_on_left, phys_left, chivC])
        # B: {chivC, j*vR} -> vL==chivC j vR
        B = np.reshape(B, [chivC, phys_right, chi_right_on_right])
        # vL [vL'] * [vL] i vR -> vL i vR
        A = np.tensordot(np.diag(self.S[i] ** (-1)), A, [1, 0])
        # vL i [vR] * [vR] vR -> vL i vR
        A = np.tensordot(A, np.diag(S), [2, 0])
        self.S[i + 1] = S
        self.B[i] = A
        self.B[i + 1] = B

    def update_bond(self, i: int, chi_max: int, eps: float):
        theta = self.get_theta2(i)
        U_bond = self.U[i]
        # i j [i*] [j*], vL [i] [j] vR
        Utheta = np.tensordot(U_bond, theta,
                              axes=([2, 3], [1, 2]))
        Utheta = np.transpose(Utheta, [2, 0, 1, 3])  # vL i j vR
        self.split_truncate_theta(Utheta, i, chi_max, eps)


class SpinBoson:

    def __init__(self, pd):
        self.pd_spin = pd[-1]
        self.pd_boson = pd[0:-1]
        self.len_boson = len(self.pd_boson)
        self.sd = lambda x: np.heaviside(x, 1) / 1. * exp(-x / 1)
        self.domain = [0, 1]
        self.he_dy = np.eye(self.pd_spin)
        self.h1e = np.eye(self.pd_spin)
        self.k_list = []
        self.w_lsit = []
        self.H = []

    def get_coupling(self, n, j, domain, g, ncap=20000):
        alphaL, betaL = rc.recurrenceCoefficients(
            n - 1, lb=domain[0], rb=domain[1], j=j, g=g, ncap=ncap
        )
        w_list = g * np.array(alphaL)
        k_list = g * np.sqrt(np.array(betaL))
        k_list[0] = k_list[0] / g
        _, _, self.h_squared = rc._j_to_hsquared(func=j, lb=domain[0], rb=domain[1], g=g)
        self.domain = domain
        return w_list, k_list

    def build_coupling(self, g, ncap):
        n = len(self.pd_boson)
        self.w_list, self.k_list = self.get_coupling(n, self.sd, self.domain, g, ncap)

    def poly(self, n, x):
        assert type(n) is int
        k = self.k_list
        w = self.w_list
        if n == -1:
            return 0
        if n == 0:
            return 1 / k[0]
        if n >= 1:
            return (1 / k[n - 1] * x - w[n - 1] / k[n - 1]) * self.poly(n - 1, x) - k[n - 1] / k[n] * self.poly(n - 2, x)

    def get_h1(self):
        w_list = self.w_list[::-1]
        h1 = []
        for i, w in enumerate(w_list):
            c = _c(self.pd_boson[i])
            h1.append(w * c.T @ c)
        h1.append(self.h1e)
        return h1

    def get_h2(self, t):
        print("Geting h2")
        h_squared = self.h_squared
        pn_list = self.pn_list
        print(pn_list)
        p1 = pn_list[1]
        print(p1(5))
        d_nt = []
        print("Geting d's")


        for p in pn_list:
            integrandReal = lambda x: h_squared(x) * p(x) * np.cos(x * t)
            print("Real Integrand")
            integrandComp = lambda x: h_squared(x) * p(x) * np.sin(-x * t)
            print("Complex Integrand")
            d_tReal, err = integrate.quad(integrandReal, *self.domain)
            print("Real Integration")
            d_tComp, err = integrate.quad(integrandComp, *self.domain)
            d_nt.append(d_tReal+1j*d_tComp)
            print("Integration Over")
        d_nt = d_nt[::-1]
        print("Integration Over")

        h2 = []
        for i, k in enumerate(d_nt):
            d1 = self.pd_boson[i]
            d2 = self.pd_spin
            c1 = _c(d1)
            kc = k.conjugate()
            print(k,c1,k*c1.T)
            coup = kron(k*c1 + kc* c1.T, self.he_dy)
            h2.append((coup, d1, d2))
        d1 = self.pd_boson[-1]
        d2 = self.pd_spin
        site = kron(np.eye(d1), self.h1e)
        h2[-1] = (h2[-1][0] + site, d1, d2)
        return h2

    def build(self, g, ncap=20000):
        self.build_coupling(g, ncap)
        print("Coupling Over")
        self.pn_list = list([lambda x: self.poly(n, x) for n in range(self.len_boson)])
        print(self.pn_list)
        # hee = self.get_h2(t)
        # print("Hamiltonian Over")
        # self.H = hee

    def get_u(self, t, dt):
        hee = self.get_h2(t)
        self.H = hee
        U = dcopy(self.H)
        for i, h_d1_d2 in enumerate(self.H):
            h, d1, d2 = h_d1_d2
            u = calc_U(h, dt).toarray()
            r0 = r1 = d1  # physical dimension for site A
            s0 = s1 = d2  # physical dimension for site B
            u = u.reshape([r0, s0, r1, s1])
            U[i] = u
            print("Exponential", i, r0 * s0, r1 * s1)
        return U
