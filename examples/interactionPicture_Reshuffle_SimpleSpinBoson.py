import numpy as np
from scipy.optimize import curve_fit
# from fishbonett.starSpinBoson import SpinBoson, SpinBoson1D
from fishbonett.backwardSpinBoson import SpinBoson, SpinBoson1D, calc_U
from fishbonett.stuff import sigma_x, sigma_z, temp_factor, sd_zero_temp, drude1, lemmer, drude, _num
from scipy.linalg import expm
from time import time

bath_length = 200
phys_dim = 20
bond_dim = 1000
a = [np.ceil(phys_dim - N*(phys_dim -2)/ bath_length) for N in range(bath_length)]
a = [int(x) for x in a]

a = [phys_dim]*bath_length
print(a)

pd = a[::-1] + [2]
eth = SpinBoson(pd)
etn = SpinBoson1D(pd)
# set the initial state of the system. It's in the high-energy state |0>:
# if you doubt this, pls check the definition of sigma_z
etn.B[-1][0, 1, 0] = 0.
etn.B[-1][0, 0, 0] = 1.


# spectral density parameters
g = 500
eth.domain = [-g, g]
temp = 226.00253972894595*0.5*1
j = lambda w: drude(w, lam=4.0*78.53981499999999/2, gam=0.25*4*19.634953749999998) * temp_factor(temp,w)

eth.sd = j

eth.he_dy = sigma_z
eth.h1e =  78.53981499999999 * sigma_x

eth.build(g=1., ncap=20000)
# print(eth.w_list,eth.k_list)
#
# print(len(eth.w_list))
# exit()

# b = np.array([np.abs(eth.get_dk(t=i*0.2/100)) for i in range(200)])

# bj, freq, coef = eth.get_dk(1, star=True)
# indexes = np.abs(freq).argsort()
# bj = bj[indexes]
# bj = np.array(bj)
# print(b.shape)

# b.astype('float32').tofile('./output/dk.dat')

# bj.astype('float32').tofile('./output/j0.dat')
# freq.astype('float32').tofile('./output/freq.dat')
# coef.astype('float32').tofile('./output/coef.dat')

# print(freq)
# print(coef)
# exit()

print(eth.w_list)
print(eth.k_list)


# U_one = eth.get_u(dt=0.002, t=0.2)

# ~ 0.5 ps ~ 0.1T
p = []


threshold = 1e-3
dt = 0.001
num_steps = 100

s_dim = np.empty([0,0])
num_l = np.empty([0,0])

t0 = time()
pos_sys = bath_length
for tn in range(num_steps):
    speed = 1
    move = int(np.floor(tn/speed))
    etn.update_on_body(eth.h1e, pos_sys, dt)

    U1_normal, U1_reverse = eth.get_u(2*tn*dt, 2*dt, factor=2, inc_sys=False)
    etn.U = U1_reverse
    for j in range(bath_length - move, bath_length, 1):
        print("j==", j, tn, "On Right, To Right")
        etn.update_bond(j, bond_dim, threshold, swap=1)

    # U2_normal, U2_reverse = eth.get_u((2*tn+1) * dt, dt, mode='reverse')
    etn.U = U1_normal
    for j in range(bath_length-1, bath_length - move -1, -1):
        print("j==", j, tn, "On Right, To Left")
        etn.update_bond(j, bond_dim, threshold, swap=1)

    ## System tensor jumps to the left end
    etn.U = U1_normal
    for j in range(bath_length-move-1, -1, -1):
        print("j==", j, tn, "On Left, To Left")
        etn.update_bond(j, bond_dim, threshold, swap=1)

    etn.U = U1_reverse
    for j in range(0, bath_length-move-1):
        print("j==", j, tn, "On Left, To Right")
        etn.update_bond(j, bond_dim, threshold, swap=1)

    print("j==", bath_length - move -1, tn, f"Moving to Left by {move+1}")
    pos_sys = bath_length-move-1
    etn.update_bond(pos_sys, bond_dim, threshold, swap=0)

    etn.update_on_body(eth.h1e, pos_sys, dt)

    dim = [len(s) for s in etn.S]
    s_dim = np.append(s_dim, dim)

    theta = etn.get_theta1(pos_sys) # c.shape vL i vR
    print(theta.shape)
    rho = np.einsum('LiR,LjR->ij',  theta, theta.conj())

    pop = np.einsum('ij,ji', rho, sigma_z)
    p = p + [pop]

    # numExp = []
    # for i, pd in enumerate(a[::-1]):
    #     theta = etn.get_theta1(i)
    #     rho = np.einsum('LiR,LjR->ij', theta, theta.conj())
    #     numExp.append(np.einsum('ij,ji', rho, _num(pd)).real)
    # num_l = np.append(num_l, numExp)
t1 = time()
print(t1-t0)
pop = [x.real for x in p]
print("population", pop)
pop = np.array(pop)

s_dim.astype('float32').tofile('./output/dim_sh.dat')
pop.astype('float32').tofile('./output/pop_sh.dat')
# num_l.astype('float32').tofile('./output/num_ic_shuffle.dat')