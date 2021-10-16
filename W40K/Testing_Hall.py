import numpy as np

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


F = lambda x: 1.6**(x-3)