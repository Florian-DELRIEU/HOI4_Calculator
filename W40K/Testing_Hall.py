import numpy as np
import matplotlib.pyplot as plt

CC_test = np.arange(6)+1
CT_test = np.arange(6)+1
F_test = np.arange(10)+1
E_test = np.arange(10)+1
PV_test = np.arange(10)+1
A_test = 1
Cd_test = np.arange(10)+1
PA_test = (np.arange(6)+1)[::-1][:-1]
Svg_test = (np.arange(6)+1)[::-1][:-1]
SvgInvu_test = (np.arange(6)+1)[::-1][:-1]
Range_test = (np.arange(6)+1)*6
Cadence_test = 1


HA = np.exp(F_test/2) /100
bonus_CC = np.exp((CC_test-3)/2.8)


plt.plot(HA,"k+")
plt.grid("both")