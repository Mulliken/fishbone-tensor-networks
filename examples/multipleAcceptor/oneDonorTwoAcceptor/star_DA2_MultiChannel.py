import numpy as np
from fishbonett.starSpinBosonMultiChannel import SpinBoson, calc_U
from fishbonett.spinBosonMPS import SpinBoson1D
from fishbonett.stuff import sigma_x, sigma_z, temp_factor, sd_zero_temp, drude1, lemmer, drude, _num, sigma_1
from time import time

bath_length = (162)*2
phys_dim = 20
bond_dim = 1000
a = [np.ceil(phys_dim - N*(phys_dim -2)/ bath_length) for N in range(bath_length)]
a = [int(x) for x in a]

a = [phys_dim]*bath_length
print(a)
pd = a[::-1] + [2]
coup_num_LE = [8.72075, 7.58513, -2.60922, 1.9799, -2.94015, 2.90197, -10.78055, 0.29698, -3.80141, 3.6713, 23.64494, -7.41048, 3.33472, 32.43075, -7.42816, 24.12083, 1.17309, -17.21169, -72.12065, -0.79479, 0.0, 9.49786, -35.06401, 31.35382, 2.06475, -3.19895, -237.99376, -14.25527, 70.5834, -12.02364, -16.11991, 37.40312, 1.64756, -23.59615, -24.8449, 88.2045, 33.50272, 3.29017, -15.01753, -6.30174, -6.56195, -13.60403, -1.67443, -17.19684, 3.0342, -1.30885, -1.75645, 1.77342, 73.40193, -75.25101, -25.25927, 8.68044, -50.1268, -78.73068, 21.5908, 3.77666, -2.71529, -25.82283, 2.20052, 47.43272, 23.86839, 13.88192, 3.49594, -55.30141, -15.97991, -16.39993, -17.71727, -38.66743, 1.25016, -16.32568, 18.25043, -21.44513, 6.32153, -25.56403, 27.82748, -1.99616, 8.86146, 24.81945, -30.37519, -51.56718, -2.12344, 2.12556, -20.05638, -4.2978, 48.75643, 37.54171, 5.92838, -8.15153, 0.0, 170.60365, -3.8007, -17.48534, -11.95364, 4.03758, 8.09637, -10.58044, 48.39439, -2.46922, -5.76646, -134.51999, 267.5091, 76.27419, 0.85843, -3.48745, 13.14158, -25.44807, -86.41269, 6.22183, 3.56382, -533.2568, -112.68242, -382.68478, 2.82984, -7.60281, 0.95106, 24.04163, 3.89757, 0.0, 445.30191, 13.05319, -129.71025, 0.0, -2.03081, -601.43038, 618.91006, -2.12273, 53.42192, 95.64043, -2.19486, -4.51983, 967.18631, 0.0, -189.92605, 2.38719, -168.79558, 16.85884, 0.0, -65.40879, -2.43386, 2.45932, 40.09578, 6.27911, -42.72198, -107.5863, 0.0, -6.75428, 2.25214, 2.25496, -9.02551, -11.31017, -2.26203, -6.78823, -15.84909, -9.07642, 2.26911, -2.27193, 4.54528, 29.54434, 0.0, -2.28113, 2.28113, 82.12055]
coup_num_CT1 = [11.64393, -51.65344, 16.58307, 47.659, 64.6833, -9.43139, -8.7759, 14.31467, 19.83859, 53.88719, 39.29605, -5.92838, -17.50726, -67.17797, -6.88793, 5.14774, 16.08809, -19.59746, -299.81045, 0.1987, 5.18451, -71.02746, -56.18953, 61.57981, 186.86004, -6.66448, 160.19363, -8.90955, 36.51924, -63.8178, -18.64853, 259.85326, -282.06207, 224.99431, -16.56327, 189.00964, 43.33504, 118.81162, 79.48304, 7.08945, -12.30366, -13.19178, -1.67443, 55.4598, -35.97689, 0.0, -36.00729, 9.75383, 86.40986, -10.28275, -33.83789, 57.86962, -168.07221, -172.28727, -129.54479, 15.64615, -20.09315, -152.18989, 12.65297, 65.08211, 15.54221, 15.61716, -157.31712, -115.30932, 21.30654, -39.48131, -21.99385, -88.56088, -67.5089, -17.5815, 60.4152, -46.6747, -13.27522, -55.06099, 80.8322, -5.3231, 14.99632, 95.14122, -9.8896, -122.20714, -77.15171, -50.30499, 225.63424, 0.7163, 58.79451, 319.82652, 10.37467, -5.18734, 4.45053, 363.45996, -12.16224, -23.04885, -7.96909, -22.61045, 37.24331, 254.74441, 214.90389, -35.39211, -106.26754, -79.87125, -11.04006, 79.70225, -2.57528, -34.00264, -3.50442, -95.64963, -116.3926, -112.88182, 26.72864, -301.28547, -66.11943, -225.27503, -73.57587, 55.12039, 25.67858, -16.34831, -1.94879, -8.83318, 302.52574, 21.08592, -84.46249, -8.10627, 35.53919, -104.91273, 28.27508, 16.98188, 129.28104, 99.98773, -131.69157, 30.50883, 446.39368, -15.22259, -223.92516, -137.26357, -366.32232, 181.83463, 41.08715, -122.33867, 127.77773, 138.95143, 32.57782, -28.8839, 958.73144, -965.74523, -22.51428, -96.8114, 268.00408, 4.50993, -187.27935, -9.04814, 2.26203, -83.72144, -206.03819, -9.07642, -2.26911, -6.8158, 199.99243, 424.9839, -9.12451, -376.38587, 22.81126, 554.31373]
coup_num_CT2 = [3.0, 17.0, 41.0, 50.0, 54.0, 57.0, 63.0, 84.0, 84.0, 88.0, 119.0, 131.0, 131.0, 156.0, 191.0, 208.0, 237.0, 241.0, 267.0, 281.0, 282.0, 292.0, 308.0, 319.0, 365.0, 377.0, 406.0, 420.0, 434.0, 436.0, 447.0, 464.0, 466.0, 470.0, 488.0, 495.0, 515.0, 517.0, 518.0, 557.0, 580.0, 583.0, 592.0, 608.0, 613.0, 617.0, 621.0, 627.0, 657.0, 661.0, 674.0, 682.0, 695.0, 723.0, 727.0, 763.0, 768.0, 777.0, 778.0, 780.0, 785.0, 818.0, 824.0, 832.0, 837.0, 859.0, 864.0, 882.0, 884.0, 888.0, 890.0, 892.0, 894.0, 927.0, 937.0, 941.0, 964.0, 975.0, 999.0, 999.0, 1001.0, 1002.0, 1013.0, 1013.0, 1014.0, 1021.0, 1048.0, 1048.0, 1049.0, 1049.0, 1075.0, 1124.0, 1127.0, 1142.0, 1145.0, 1151.0, 1160.0, 1164.0, 1165.0, 1189.0, 1201.0, 1212.0, 1214.0, 1233.0, 1239.0, 1241.0, 1247.0, 1257.0, 1260.0, 1307.0, 1317.0, 1333.0, 1334.0, 1344.0, 1345.0, 1360.0, 1378.0, 1388.0, 1412.0, 1420.0, 1422.0, 1433.0, 1436.0, 1469.0, 1481.0, 1501.0, 1511.0, 1537.0, 1552.0, 1598.0, 1644.0, 1656.0, 1658.0, 1688.0, 1693.0, 1703.0, 1709.0, 1713.0, 1721.0, 1739.0, 1772.0, 1776.0, 1777.0, 1790.0, 3184.0, 3184.0, 3185.0, 3189.0, 3191.0, 3199.0, 3199.0, 3200.0, 3202.0, 3209.0, 3209.0, 3213.0, 3214.0, 3214.0, 3226.0, 3226.0, 3226.0, 3226.0]
freq_num = [3.0, 17.0, 41.0, 50.0, 54.0, 57.0, 63.0, 84.0, 84.0, 88.0, 119.0, 131.0, 131.0, 156.0, 191.0, 208.0, 237.0, 241.0, 267.0, 281.0, 282.0, 292.0, 308.0, 319.0, 365.0, 377.0, 406.0, 420.0, 434.0, 436.0, 447.0, 464.0, 466.0, 470.0, 488.0, 495.0, 515.0, 517.0, 518.0, 557.0, 580.0, 583.0, 592.0, 608.0, 613.0, 617.0, 621.0, 627.0, 657.0, 661.0, 674.0, 682.0, 695.0, 723.0, 727.0, 763.0, 768.0, 777.0, 778.0, 780.0, 785.0, 818.0, 824.0, 832.0, 837.0, 859.0, 864.0, 882.0, 884.0, 888.0, 890.0, 892.0, 894.0, 927.0, 937.0, 941.0, 964.0, 975.0, 999.0, 999.0, 1001.0, 1002.0, 1013.0, 1013.0, 1014.0, 1021.0, 1048.0, 1048.0, 1049.0, 1049.0, 1075.0, 1124.0, 1127.0, 1142.0, 1145.0, 1151.0, 1160.0, 1164.0, 1165.0, 1189.0, 1201.0, 1212.0, 1214.0, 1233.0, 1239.0, 1241.0, 1247.0, 1257.0, 1260.0, 1307.0, 1317.0, 1333.0, 1334.0, 1344.0, 1345.0, 1360.0, 1378.0, 1388.0, 1412.0, 1420.0, 1422.0, 1433.0, 1436.0, 1469.0, 1481.0, 1501.0, 1511.0, 1537.0, 1552.0, 1598.0, 1644.0, 1656.0, 1658.0, 1688.0, 1693.0, 1703.0, 1709.0, 1713.0, 1721.0, 1739.0, 1772.0, 1776.0, 1777.0, 1790.0, 3184.0, 3184.0, 3185.0, 3189.0, 3191.0, 3199.0, 3199.0, 3200.0, 3202.0, 3209.0, 3209.0, 3213.0, 3214.0, 3214.0, 3226.0, 3226.0, 3226.0, 3226.0]

back_coup  = [1.76783972e-10, 4.10444212e-09, 4.38923621e-08, 3.04210601e-07,
       1.57146407e-06, 6.52538999e-06, 2.28322968e-05, 6.95130658e-05,
       1.88461395e-04, 4.63029925e-04, 1.04506040e-03, 2.19051571e-03,
       4.30208482e-03, 7.97508786e-03, 1.40411527e-02, 2.36029230e-02,
       3.80528385e-02, 5.90699458e-02, 8.85906646e-02, 1.28752160e-01,
       1.81810026e-01, 2.50034922e-01, 3.35595175e-01, 4.40433950e-01,
       5.66150122e-01, 7.13891620e-01, 8.84268773e-01, 1.07729331e+00,
       1.29234650e+00, 1.52817761e+00, 1.78293169e+00, 2.05420415e+00,
       2.33911790e+00, 2.63441873e+00, 2.93658392e+00, 3.24193994e+00,
       3.54678572e+00, 3.84751914e+00, 4.14076538e+00, 4.42350646e+00,
       4.69321134e+00, 4.94796476e+00, 5.18659139e+00, 5.40876788e+00,
       5.61511158e+00, 5.80722999e+00, 5.98771075e+00, 6.16003088e+00,
       6.32836684e+00, 6.49729763e+00, 6.67141098e+00, 6.85484734e+00,
       7.05084015e+00, 7.26132502e+00, 7.48668637e+00, 7.72568579e+00,
       7.97557990e+00, 8.23239935e+00, 8.49133761e+00, 8.74719167e+00,
       8.99480459e+00, 9.22947381e+00, 9.44730374e+00, 9.64549172e+00,
       9.82254227e+00, 9.97840623e+00, 1.01145398e+01, 1.02338762e+01,
       1.03407014e+01, 1.04404227e+01, 1.05392295e+01, 1.06436485e+01,
       1.07600216e+01, 1.08939478e+01, 1.10497540e+01, 1.12300668e+01,
       1.14355471e+01, 1.16648244e+01, 1.19146305e+01, 1.21800977e+01,
       1.24551620e+01, 1.27330091e+01, 1.30065082e+01, 1.32685951e+01,
       1.35125851e+01, 1.37324095e+01, 1.39227795e+01, 1.40792860e+01,
       1.41984474e+01, 1.42777139e+01, 1.43154405e+01, 1.43108352e+01,
       1.42638901e+01, 1.41753016e+01, 1.40463826e+01, 1.38789730e+01,
       1.36753488e+01, 1.34381346e+01, 1.31702194e+01, 1.28746782e+01,
       1.25547006e+01, 1.22135257e+01, 1.18543854e+01, 1.14804549e+01,
       1.10948111e+01, 1.07003977e+01, 1.02999985e+01, 9.89621603e+00,
       9.49145650e+00, 9.08792036e+00, 8.68759716e+00, 8.29226478e+00,
       7.90349200e+00, 7.52264402e+00, 7.15089034e+00, 6.78921446e+00,
       6.43842497e+00, 6.09916764e+00, 5.77193810e+00, 5.45709483e+00,
       5.15487219e+00, 4.86539329e+00, 4.58868244e+00, 4.32467719e+00,
       4.07323965e+00, 3.83416723e+00, 3.60720255e+00, 3.39204267e+00,
       3.18834742e+00, 2.99574706e+00, 2.81384914e+00, 2.64224460e+00,
       2.48051318e+00, 2.32822822e+00, 2.18496075e+00, 2.05028308e+00,
       1.92377183e+00, 1.80501046e+00, 1.69359144e+00, 1.58911791e+00,
       1.49120511e+00, 1.39948139e+00, 1.31358907e+00, 1.23318492e+00,
       1.15794056e+00, 1.08754258e+00, 1.02169261e+00, 9.60107152e-01,
       9.02517416e-01, 8.48668971e-01, 7.98321393e-01, 7.51247829e-01,
       7.07234520e-01, 6.66080302e-01, 6.27596074e-01, 5.91604260e-01,
       5.57938261e-01, 5.26441908e-01, 4.96968916e-01, 4.69382354e-01,
       4.43554115e-01, 4.19364408e-01, 3.96701264e-01, 3.75460058e-01,
       3.55543048e-01, 3.36858938e-01, 3.19322451e-01, 3.02853931e-01,
       2.87378954e-01, 2.72827966e-01, 2.59135928e-01, 2.46241989e-01,
       2.34089163e-01, 2.22624028e-01, 2.11796435e-01, 2.01559225e-01,
       1.91867960e-01, 1.82680657e-01, 1.73957527e-01, 1.65660715e-01,
       1.57754035e-01, 1.50202702e-01, 1.42973039e-01, 1.36032174e-01,
       1.29347691e-01, 1.22887231e-01, 1.16618027e-01, 1.10506322e-01,
       1.04516628e-01, 9.86107530e-02, 9.27464570e-02, 8.68755234e-02,
       8.09408718e-02, 7.48719930e-02, 6.85772755e-02, 6.19300682e-02,
       5.47406482e-02, 4.66911122e-02, 3.71460374e-02, 2.43093082e-02]

back_freq = [  0.63503484,   0.83242449,   1.03233903,   1.24251728,
         1.46583262,   1.70380051,   1.95738665,   2.22728314,
         2.51402528,   2.81804841,   3.13971858,   3.47935036,
         3.83721799,   4.21356266,   4.60859753,   5.02251137,
         5.45547124,   5.90762457,   6.37910082,   6.87001282,
         7.38045793,   7.91051895,   8.46026502,   9.02975233,
         9.61902485,  10.22811487,  10.85704369,  11.5058221 ,
        12.17445101,  12.86292197,  13.57121777,  14.29931308,
        15.04717518,  15.8147647 ,  16.60203659,  17.40894112,
        18.23542501,  19.08143271,  19.94690752,  20.83179269,
        21.73603194,  22.65956924,  23.60234741,  24.56430477,
        25.54536959,  26.54545172,  27.56443126,  28.60214505,
        29.65837221,  30.73282143,  31.82512341,  32.93483198,
        34.0614361 ,  35.20438236,  36.36310471,  37.53705578,
        38.72573378,  39.9287009 ,  41.14559158,  42.37611175,
        43.62003153,  44.87717409,  46.147403  ,  47.43060923,
        48.72669837,  50.03557796,  51.35714443,  52.69126918,
        54.03778382,  55.39646478,  56.76701885,  58.14907169,
        59.54216224,  60.94574579,  62.3592073 ,  63.78188437,
        65.21309681,  66.65217759,  68.09849992,  69.55149637,
        71.01066818,  72.47558553,  73.94588108,  75.42123938,
        76.9013849 ,  78.38607035,  79.87506646,  81.36815364,
        82.86511557,  84.36573452,  85.86978813,  87.37704724,
        88.88727466,  90.40022452,  91.91564201,  93.43326348,
        94.9528167 ,  96.47402121,  97.99658878,  99.52022391,
       101.04462423, 102.56948109, 104.09447992, 105.61930073,
       107.14361849, 108.66710354, 110.18942198, 111.71023597,
       113.22920409, 114.74598164, 116.26022094, 117.77157156,
       119.27968067, 120.78419319, 122.28475207, 123.78099855,
       125.27257233, 126.75911177, 128.24025416, 129.71563584,
       131.18489245, 132.64765908, 134.10357046, 135.55226114,
       136.99336568, 138.42651878, 139.85135548, 141.26751131,
       142.67462248, 144.07232598, 145.46025979, 146.83806302,
       148.20537605, 149.56184071, 150.90710039, 152.24080021,
       153.5625872 , 154.87211036, 156.16902089, 157.45297228,
       158.72362047, 159.98062399, 161.22364406, 162.45234481,
       163.66639331, 164.8654598 , 166.04921774, 167.217344  ,
       168.36951895, 169.50542661, 170.62475476, 171.7271951 ,
       172.8124433 , 173.8801992 , 174.93016688, 175.96205478,
       176.97557585, 177.97044762, 178.94639233, 179.90313707,
       180.84041383, 181.75795965, 182.6555167 , 183.53283241,
       184.38965953, 185.22575626, 186.04088635, 186.83481914,
       187.60732974, 188.35819902, 189.08721377, 189.79416677,
       190.47885683, 191.14108892, 191.78067421, 192.39743019,
       192.99118068, 193.56175594, 194.10899272, 194.63273436,
       195.13283077, 195.60913858, 196.06152114, 196.48984858,
       196.89399787, 197.27385288, 197.62930439, 197.96025016,
       198.26659495, 198.54825058, 198.80513593, 199.03717701,
       199.24430697, 199.42646611, 199.58360194, 199.71566921,
       199.82262995, 199.90445368, 199.96111833, 199.99262015]


coup_num_LE = coup_num_LE #+ list([1.15*x for x in back_coup])
coup_num_CT1 = coup_num_CT1 #+ list([-1.15*x for x in back_coup])
# coup_num_CT1 = coup_num_CT1 + list([-1.15*x for x in back_coup])

coup_mat = [np.diag([x, y]) for x, y in zip(coup_num_LE, coup_num_CT1)]
freq_num = freq_num #+ back_freq
reorg = sum([(coup_num_LE[i]-coup_num_CT1[i]) ** 2 / freq_num[i] for i in range(len(freq_num))])
print("Reorg",reorg)
print(f"Len {len(coup_mat)}")
# exit()
temp = 5
eth = SpinBoson(pd, coup_mat=coup_mat, freq=freq_num, temp=temp)
etn = SpinBoson1D(pd)

# set the initial state of the system. It's in the high-energy state |0>:
# if you doubt this, pls check the definition of sigma_z
etn.B[-1][0, 1, 0] = 0.
etn.B[-1][0, 0, 0] = 1.


# spectral density parameters

eth.h1e =  3*134.56223*sigma_x + np.diag([0, -2000])

# eth.build(n=0)
# exit()
# print(eth.w_list,eth.k_list)
#
# print(len(eth.w_list))
# exit()

# b = np.array([np.abs(eth.get_dk(t=i*0.2/100)) for i in range(100)])
# print(b.shape)
# bj, freq, coef = eth.get_dk(1, star=True)
# coef = eth.get_dk(1, star=True)
# indexes = np.abs(freq).argsort()
# bj = bj[indexes]
# bj = np.array(bj)
# print(b.shape)
# b.astype('float32').tofile('./DA2/dk.dat')
# bj.astype('float32').tofile('./output/j0.dat')
# freq.astype('float32').tofile('./output/freq.dat')
# coup_num = np.array([[freq_num[n], coup_num[n]] for n in range(len(freq_num))])
# coup_num.astype('float32').tofile('./DA2/coup.dat')
# spacing = [freq_num[i+1]-freq_num[i] for i in range(161)]
# rms = np.sqrt(sum([x**2 for x in spacing])/161)
# print(rms)
# coef.astype('float32').tofile('./DA2/coef.dat')

# print(freq)
# print(coef)
# exit()


# U_one = eth.get_u(dt=0.002, t=0.2)

# ~ 0.5 ps ~ 0.1T
p = []


threshold = 1e-3
dt = 0.001/8
num_steps = 50*4

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

    pop = np.einsum('ij,ji', rho, sigma_z)
    p = p + [pop]
    t1 = time()
    t = t + t1 - t0
tt1 = time()
print(tt1-tt0)
pop = [x.real for x in p]
print("population", pop)
pop = np.array(pop)

# s_dim.astype('float32').tofile('./output/dim.dat')
# pop.astype('float32').tofile('./output/pop.dat')
# num_l.astype('float32').tofile('./output/num_ic.dat')