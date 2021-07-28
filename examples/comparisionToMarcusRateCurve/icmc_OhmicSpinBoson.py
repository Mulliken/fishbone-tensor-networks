import numpy as np
from fishbonett.backwardSpinBosonMultiChannel import SpinBoson, SpinBoson1D, calc_U
from fishbonett.stuff import sigma_x, sigma_z, temp_factor, sd_zero_temp, drude1, lemmer, drude, _num, sigma_1
from time import time

bath_length = 300
phys_dim = 10
bond_dim = 1000
a = [phys_dim]*bath_length
print(a)
pd = a[::-1] + [2]
coup_num = [0.00055425, 0.00136128, 0.00237097, 0.00354767, 0.00486874,
       0.00631789, 0.00788243, 0.00955199, 0.01131773, 0.01317189,
       0.01510752, 0.01711831, 0.01919838, 0.02134226, 0.02354478,
       0.02580102, 0.02810628, 0.03045603, 0.0328459 , 0.03527169,
       0.0377293 , 0.04021474, 0.04272414, 0.04525373, 0.04779983,
       0.05035886, 0.05292733, 0.0555018 , 0.05807898, 0.0606556 ,
       0.06322853, 0.06579468, 0.06835107, 0.0708948 , 0.07342306,
       0.07593311, 0.07842231, 0.08088812, 0.08332806, 0.08573977,
       0.08812095, 0.09046943, 0.09278308, 0.09505992, 0.09729802,
       0.09949556, 0.1016508 , 0.10376212, 0.10582796, 0.10784689,
       0.10981753, 0.11173863, 0.113609  , 0.11542758, 0.11719335,
       0.11890542, 0.12056297, 0.12216528, 0.12371169, 0.12520165,
       0.12663468, 0.12801038, 0.12932844, 0.13058861, 0.13179074,
       0.13293473, 0.13402057, 0.13504829, 0.13601804, 0.13692997,
       0.13778435, 0.13858147, 0.1393217 , 0.14000547, 0.14063324,
       0.14120555, 0.14172295, 0.14218609, 0.1425956 , 0.14295221,
       0.14325665, 0.14350971, 0.14371219, 0.14386495, 0.14396885,
       0.1440248 , 0.14403372, 0.14399657, 0.1439143 , 0.14378792,
       0.14361841, 0.1434068 , 0.14315411, 0.14286138, 0.14252966,
       0.14216   , 0.14175345, 0.14131108, 0.14083393, 0.14032308,
       0.13977956, 0.13920445, 0.13859877, 0.13796358, 0.1372999 ,
       0.13660875, 0.13589115, 0.1351481 , 0.13438057, 0.13358956,
       0.132776  , 0.13194086, 0.13108505, 0.13020948, 0.12931504,
       0.1284026 , 0.12747303, 0.12652715, 0.12556576, 0.12458968,
       0.12359965, 0.12259644, 0.12158077, 0.12055333, 0.11951482,
       0.11846588, 0.11740716, 0.11633925, 0.11526275, 0.11417822,
       0.11308619, 0.11198718, 0.11088167, 0.10977014, 0.10865301,
       0.1075307 , 0.10640361, 0.10527209, 0.10413649, 0.10299712,
       0.10185427, 0.1007082 , 0.09955915, 0.09840733, 0.09725293,
       0.0960961 , 0.09493699, 0.0937757 , 0.09261231, 0.09144688,
       0.09027942, 0.08910995, 0.08793842, 0.08676477, 0.08558893,
       0.08441076, 0.08323011, 0.0820468 , 0.08086061, 0.07967128,
       0.07847852, 0.077282  , 0.07608135, 0.07487615, 0.07366595,
       0.07245023, 0.07122843, 0.06999993, 0.06876405, 0.06752004,
       0.0662671 , 0.06500431, 0.0637307 , 0.06244517, 0.06114655,
       0.05983351, 0.05850459, 0.0571582 , 0.05579254, 0.05440562,
       0.05299519, 0.05155874, 0.05009341, 0.04859595, 0.04706261,
       0.04548908, 0.0438703 , 0.04220028, 0.0404719 , 0.03867649,
       0.03680333, 0.03483895, 0.03276593, 0.03056108, 0.02819233,
       0.02561292, 0.02274987, 0.01947684, 0.01553515, 0.01018117]
freq_num = [2.70523917e-04, 9.06815746e-04, 1.90669652e-03, 3.26985006e-03,
       4.99593709e-03, 7.08454138e-03, 9.53516254e-03, 1.23472145e-02,
       1.55200251e-02, 1.90528362e-02, 2.29448035e-02, 2.71949970e-02,
       3.18024011e-02, 3.67659148e-02, 4.20843517e-02, 4.77564407e-02,
       5.37808259e-02, 6.01560674e-02, 6.68806409e-02, 7.39529386e-02,
       8.13712693e-02, 8.91338591e-02, 9.72388513e-02, 1.05684307e-01,
       1.14468206e-01, 1.23588447e-01, 1.33042847e-01, 1.42829144e-01,
       1.52944995e-01, 1.63387978e-01, 1.74155593e-01, 1.85245262e-01,
       1.96654328e-01, 2.08380059e-01, 2.20419644e-01, 2.32770199e-01,
       2.45428764e-01, 2.58392305e-01, 2.71657712e-01, 2.85221805e-01,
       2.99081330e-01, 3.13232962e-01, 3.27673306e-01, 3.42398895e-01,
       3.57406194e-01, 3.72691600e-01, 3.88251442e-01, 4.04081982e-01,
       4.20179415e-01, 4.36539873e-01, 4.53159423e-01, 4.70034069e-01,
       4.87159752e-01, 5.04532351e-01, 5.22147687e-01, 5.40001519e-01,
       5.58089548e-01, 5.76407418e-01, 5.94950718e-01, 6.13714977e-01,
       6.32695674e-01, 6.51888232e-01, 6.71288022e-01, 6.90890365e-01,
       7.10690530e-01, 7.30683739e-01, 7.50865162e-01, 7.71229928e-01,
       7.91773114e-01, 8.12489757e-01, 8.33374849e-01, 8.54423338e-01,
       8.75630134e-01, 8.96990105e-01, 9.18498080e-01, 9.40148853e-01,
       9.61937179e-01, 9.83857780e-01, 1.00590534e+00, 1.02807452e+00,
       1.05035994e+00, 1.07275619e+00, 1.09525784e+00, 1.11785943e+00,
       1.14055546e+00, 1.16334042e+00, 1.18620879e+00, 1.20915499e+00,
       1.23217344e+00, 1.25525856e+00, 1.27840471e+00, 1.30160627e+00,
       1.32485759e+00, 1.34815300e+00, 1.37148683e+00, 1.39485338e+00,
       1.41824696e+00, 1.44166186e+00, 1.46509238e+00, 1.48853278e+00,
       1.51197735e+00, 1.53542036e+00, 1.55885608e+00, 1.58227877e+00,
       1.60568273e+00, 1.62906221e+00, 1.65241150e+00, 1.67572488e+00,
       1.69899665e+00, 1.72222109e+00, 1.74539253e+00, 1.76850528e+00,
       1.79155368e+00, 1.81453206e+00, 1.83743480e+00, 1.86025626e+00,
       1.88299086e+00, 1.90563299e+00, 1.92817710e+00, 1.95061765e+00,
       1.97294911e+00, 1.99516601e+00, 2.01726286e+00, 2.03923423e+00,
       2.06107472e+00, 2.08277894e+00, 2.10434154e+00, 2.12575721e+00,
       2.14702068e+00, 2.16812669e+00, 2.18907004e+00, 2.20984557e+00,
       2.23044814e+00, 2.25087267e+00, 2.27111411e+00, 2.29116747e+00,
       2.31102778e+00, 2.33069013e+00, 2.35014967e+00, 2.36940159e+00,
       2.38844111e+00, 2.40726352e+00, 2.42586417e+00, 2.44423845e+00,
       2.46238180e+00, 2.48028974e+00, 2.49795782e+00, 2.51538166e+00,
       2.53255695e+00, 2.54947942e+00, 2.56614487e+00, 2.58254917e+00,
       2.59868825e+00, 2.61455810e+00, 2.63015477e+00, 2.64547440e+00,
       2.66051318e+00, 2.67526736e+00, 2.68973329e+00, 2.70390737e+00,
       2.71778606e+00, 2.73136593e+00, 2.74464359e+00, 2.75761573e+00,
       2.77027913e+00, 2.78263064e+00, 2.79466718e+00, 2.80638575e+00,
       2.81778344e+00, 2.82885740e+00, 2.83960488e+00, 2.85002320e+00,
       2.86010976e+00, 2.86986205e+00, 2.87927764e+00, 2.88835417e+00,
       2.89708939e+00, 2.90548112e+00, 2.91352726e+00, 2.92122580e+00,
       2.92857483e+00, 2.93557252e+00, 2.94221711e+00, 2.94850694e+00,
       2.95444045e+00, 2.96001616e+00, 2.96523268e+00, 2.97008869e+00,
       2.97458299e+00, 2.97871446e+00, 2.98248207e+00, 2.98588487e+00,
       2.98892201e+00, 2.99159275e+00, 2.99389640e+00, 2.99583239e+00,
       2.99740025e+00, 2.99859959e+00, 2.99943012e+00, 2.99989184e+00]

coup_mat = [np.diag([x, -x]) for x, y in zip(coup_num, coup_num)]
# freq_num = [6.115, 19.75, 42.785, 53.035, 59.049, 62.948, 83.663, 87.539, 120.173, 131.58, 143.899, 148.496, 159.891, 201.192, 215.966, 236.831, 278.94, 282.06, 294.762, 303.878, 326.674, 342.415, 390.459, 396.117, 403.132, 409.609, 429.697, 449.173, 457.858, 469.744, 475.314, 489.934, 495.985, 514.18, 515.125, 533.989, 556.77, 579.688, 581.172, 603.909, 607.718, 624.123, 646.965, 655.423, 659.333, 665.403, 670.972, 688.064, 696.46, 719.703, 744.377, 763.996, 777.71, 780.284, 785.892, 787.852, 793.612, 811.478, 817.532, 831.652, 838.931, 842.258, 859.346, 873.155, 886.345, 888.753, 889.866, 890.658, 905.02, 920.056, 938.208, 940.357, 948.667, 966.807, 977.952, 995.335, 999.164, 1001.667, 1004.16, 1007.414, 1013.639, 1015.056, 1020.89, 1033.982, 1046.905, 1047.962, 1048.283, 1063.799, 1123.949, 1132.104, 1144.712, 1149.057, 1156.337, 1161.604, 1163.757, 1181.27, 1185.69, 1190.34, 1201.471, 1207.704, 1213.014, 1227.291, 1227.998, 1230.663, 1242.207, 1247.526, 1251.137, 1258.572, 1306.564, 1316.516, 1333.095, 1340.534, 1344.534, 1347.979, 1355.751, 1362.395, 1385.265, 1412.373, 1423.885, 1432.681, 1435.431, 1469.188, 1481.761, 1500.239, 1510.151, 1516.427, 1524.746, 1539.361, 1553.56, 1597.505, 1643.892, 1655.17, 1656.462, 1666.857, 1685.082, 1696.391, 1698.825, 1708.27, 1712.974, 1727.554, 1768.309, 1780.63, 3163.355, 3164.762, 3186.09, 3189.269, 3190.201, 3191.791, 3194.869, 3196.625, 3197.522, 3199.217, 3199.423, 3206.869, 3207.606, 3210.26, 3213.09, 3213.323, 3218.568, 3224.412, 3225.867, 3226.448]
# reorg = sum([(coup_num_1[i]-coup_num_2[i]) ** 2 / freq_num[i] for i in range(len(freq_num))])

# print("Reorg",reorg)
# exit()
temp = 1/0.6950348009119888
eth = SpinBoson(pd, coup_mat=coup_mat, freq=freq_num, temp=temp)

etn = SpinBoson1D(pd)
# set the initial state of the system. It's in the high-energy state |0>:
# if you doubt this, pls check the definition of sigma_z
etn.B[-1][0, 1, 0] = 0.
etn.B[-1][0, 0, 0] = 1.


# spectral density parameters

eth.h1e =  0.5 * sigma_x

eth.build(n=0)
# exit()
# print(eth.w_list,eth.k_list)
#
# print(len(eth.w_list))
# exit()

# b = np.array([np.abs(eth.get_dk(t=i*0.2/100)) for i in range(100)])
# print(b.shape)
# reorg = eth.get_dk(1, star=True)

# print(reorg)
# exit()
# coef = eth.get_dk(1, star=True)
# indexes = np.abs(freq).argsort()
# bj = bj[indexes]
# bj = np.array(bj)
# print(b.shape)
# b.astype('float32').tofile('./DA2/dk.dat')
# bj.astype('float32').tofile('./output/j0.dat')
# freq.astype('float32').tofile('./output/freq.dat')
# coef.astype('float32').tofile('./DA2/coef.dat')

# print(freq)
# print(coef)
# exit()


# U_one = eth.get_u(dt=0.002, t=0.2)

# ~ 0.5 ps ~ 0.1T
p = []


threshold = 1e-3
dt = 0.05
num_steps = 200

s_dim = np.empty([0,0])
num_l = np.empty([0,0])
t = 0.
tt0=time()
for tn in range(num_steps):
    U1, U2 = eth.get_u(2*tn*dt, 2*dt, factor=2)

    t0 = time()
    etn.U = U1
    for j in range(bath_length-1,0,-1):
        print("j==", j, tn)
        etn.update_bond(j, bond_dim, threshold, swap=1)

    etn.update_bond(0, bond_dim, threshold, swap=0)
    etn.update_bond(0, bond_dim, threshold, swap=0)
    t1 = time()
    t = t + t1 - t0

    t0 = time()
    etn.U = U2
    for j in range(1, bath_length):
        print("j==", j, tn)
        etn.update_bond(j, bond_dim, threshold,swap=1)

    dim = [len(s) for s in etn.S]
    s_dim = np.append(s_dim, dim)
    print("Length", len(dim))
    theta = etn.get_theta1(bath_length) # c.shape vL i vR
    rho = np.einsum('LiR,LjR->ij',  theta, theta.conj())
    sigma_z = np.diag([1,0])
    pop = np.einsum('ij,ji', rho, sigma_z)
    p = p + [pop]
    t1 = time()
    t = t + t1 - t0

tt1 = time()
print(tt1-tt0)
pop = [x.real for x in p]
print("population", pop)
pop = np.array(pop)