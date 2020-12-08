import numpy as np
import sys
from numpy import exp


def _c(dim: int):
    """
    Creates the annihilation operator
    Args:
        dim (int):
            Dimension of the site it should act on
    Returns:
        numpy.ndarray:
            The annihilation operator
    """
    op = np.zeros((dim, dim))
    for i in range(dim - 1):
        op[i, i + 1] = np.sqrt(i + 1)
    return op


class FinshBone:

    @property
    def H(self):
        self._H = self.fill_h_list()
        return self._H

    @property
    def sd(self):
        return self._sd
    #
    @property
    def He(self):
        return self._He
    @He.setter
    def He(self,m):
        self._He = m
    #
    @property
    def Hv(self):
        return self.Hv
    @Hv.setter
    def Hv(self,m):
        # check type
        self._Hv = m

    @property
    def Hee(self):
        return self._Hee
    @Hee.setter
    def Hee(self,m):
        # check type
        self._Hee = m

    @property
    def Hev(self):
        return self._Hev
    @Hev.setter
    def Hev(self,m):
        # check type
        self._Hev = m

    @property
    def He_dy(self):
        return self._He_dy
    @He_dy.setter
    def He_dy(self,m):
        # check type
        self._He_dy = m

    @property
    def Hv_dy(self):
        return self._Hv_dy
    @Hv_dy.setter
    def Hv_dy(self,m):
        # check type
        self._Hv_dy = m

    def __init__(self, pd: np.ndarray):
        """
        TODO
        :type pd: nd.ndarray
        :param pd: is a list.
         pD[0] contains physical dimensions of eb, ev, vb on the first chain,
         pD[1] contains physical dimensions of eb, ev, vb on the second chain,
         etc.
        """
        self.pd = pd
        self._nc  = len(pd) # an int
        # pD is a np.ndarray.
        self._ebL = [len(x) for x in pd[:, 0]]
        # pD[:,0] is the first column of the array, the eb column
        self._eL = [len(x) for x in pd[:, 1]]
        self._vl = [len(x) for x in pd[:, 2]]
        self._evL = self._eL + self._vL
        # pD[:,1] is the second column of the array, the ev column
        self._vbL = [len(x) for x in pd[:, 3]]
        # pD[:,2] is the third column of the array, the vb column
        self._L = [sum(x) for x in zip(self._ebL,self._evL,self._vbL)]
        self._ebD = self.pd[:, 0]
        self._evD = self.pd[:, 1]
        self._vbD = self.pd[:, 2]
        # PLEASE NOTE THE SHAPE of pd and nd.array structure.
        # pd = nd.array([
        # [eb0, ev0, vb0], [eb1, ev1, vb1], [eb2, ev2, vb2]
        # ])
        # | eb0 ev0 vb0 |
        # | eb1 ev1 vb1 |
        # | eb2 ev2 vb2 | is different from the structure depicted in SimpleTTS class.

        self._sd = np.empty([2, self._nc], dtype=object)

        #TODO two lists. w is frequency, k is coupling. Get them
        # from the get_coupling function below
        self.w_list = np.empty([2, self._nc], dtype=object)
        self.k_list = np.empty([2, self._nc], dtype=object)

        # initialize spectral densities.
        for n in range(self._nc):
            if self._evL[n] == 2:
                self.sd[0, n] = self.sd[0, n] = lambda x: 1./1. * exp(-x/1)
            elif self._evL[n] ==1 :
                self.sd[0,n] = lambda x: 1./1. * exp(-x/1)
            else:
                raise SystemError # TODO tell users what happens.
                # TODO Must hvae p-leg dims for e and v. Use 0 if v not existent.

        # Assign the matrices below according to self.pd
        self._H     = [] # list -> all bond Hamiltonians
        # _H = [ [Heb00, Heb01, ..., Hev0, Hvb00, Hvb01, ..., Hvb0N, Hee0],
        #        [Heb10, Heb11, ..., Hev1, Hvb00, Hvb01, ..., Hvb0N, Hee1],
        #        [Heb00, Heb01, ..., Hev1, Hvb00, Hvb01, ..., Hvb0N, None]
        #      ] in the case of 3 chains.
        self._H1    = []
        #self._H2 ==self._H
        self._He    = []  # list -> single Hamiltonian on e site
        self._Hv    = []  # list -> single Hamiltonian on v site
        self._Hee   = [] # list -> coupling Hamiltonian on e and e
        self._Hev   = [] # list -> coupling Hamiltonian on e and v
        self._He_dy = [] # list -> e dynamic variables coupled to eb
        self._Hv_dy = [] # list -> v dynamic variables coupled to vb

    def get_coupling(self):
        # TODO Get w and k for each spectral density
        # TODO w and k have the same structures as  self.sd (spectral densities)
        self.w_list = []
        self.k_list = []
        return self.w_list, self.k_list

    def get_h1(self, n) -> tuple:
        """

        :param n:
        :type n:
        :return:
        :rtype:
        """
        if 0 <= n <= self._nc -1:
            w_list = self.w_list[n][0]
            pd = self.pd[n, 0] # -> Physical dimensions of sites ->
            # on eb of the nth chain.
            # n -> the nth chain, 0 -> the 1st element -> w_list for eb.
            try:
                assert len(pd) == len(w_list)
            except AssertionError:
                print("Lengths of the w and pd don't match. ", file=sys.stderr)
                raise
                sys.exit(1)
            # EB Hamiltonian list
            H_eb = [None] * len(pd)
            for i, w in enumerate(w_list):
                c = _c(pd[-1-i])
                H_eb[-1-i] = w * c@c.T

            w_list = self.w_list[n][1]
            pd = self.pd[n, 2]
            # n -> the nth chain, 0 -> the 3rd element -> w_list for vb.
            try:
                assert len(pd) == len(w_list)
            except AssertionError:
                print("Lengths of the w and pd don't match. ", file=sys.stderr)
                raise
                sys.exit(1)
            # VB Hamiltonian list on the chain n
            H_vb = [None] * len(pd)
            for i, w in enumerate(w_list):
                c = _c(pd[i])
                H_vb[i] = w * c@c.T

            # EV single Hamiltonian list on the chain n
            H_ev = self.He[n] + self.Hv[n]
            return H_eb, H_ev, H_vb
        else:
            raise ValueError

    def get_h2(self, n):
        if n == -1:
            return self._Hee
        if 0 <= n <= self._nc <1:
            h1eb, h1ev, h1vb = self.get_h1(n)

            pd = self.pd[n, 0]
            kL = self.k_list[n][0]; wL = self.w_list[n][0]
            # kL is a list of k's (coupling constants) 0 indicates eb
            k0, kn = kL[0], kL[1:]; w0 = wL[0]
            kn.reverse()
            h2eb = []
            for i, k in enumerate(kn):
                m, n = pd[i], pd[i+1]
                cm = _c(m); cn = _c(n)
                h1 = h1eb[i]
                h2 = h1 + k * (np.kron(cm, cn.T)) + np.kron(cm.T, cn)
                h2 = h2.reshape(m,n,m,n)
                h2eb.append(h2)
            h2eb.append(w0*np.eye(pd[-1]))

            pd = self.pd[n, 2] # 2 indicates the vb list
            kL = self.k_list[n][1]; wL = self.w_list[n][1]
            # kL is a list of k's (coupling constants) 0 indicates eb
            k0, kn = kL[0], kL[1:]; w0 = wL[0]
            h2vb = [w0 * _c(1) @ _c(pd[0])]
            for i, k in enumerate(kn):
                m, n = pd[i], pd[i + 1]
                cm = _c(m); cn = _c(n)
                h1 = h1vb[i]
                h2 = h1 + k * (np.kron(cm, cn.T)) + np.kron(cm.T, cn)
                h2 = h2.reshape(m, n, m, n)
                h2vb.append(h2)

            # TODO. Calculate h2ev
            h2ev = []
            return h2eb + h2ev + h2vb

    def fill_h_list(self, k_list, w_list):
        # TODO Gotta check the existences of Hee Hev H_dy's and stuff.
        H = []
        hee = self.get_h2(-1)
        for n in range(self._nc):
            h = self.get_h2(n)
            H.append(h)
        for n in range(self._nc -1):
            H[n].append(hee[n])
        return H
        


class VibronicBath:
    pass
