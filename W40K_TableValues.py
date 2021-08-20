from W40K_UnitCreator import *

############ HARD & SOFT ATTACK
SoftAttack_F = dict()
SoftAttack_F[1] = 10
SoftAttack_F[2] = 11
SoftAttack_F[3] = 12.1
SoftAttack_F[4] = 13.3
SoftAttack_F[5] = 14.6
SoftAttack_F[6] = 15.4
SoftAttack_F[7] = 16.1
SoftAttack_F[8] = 16.9
SoftAttack_F[9] = 17.3
SoftAttack_F[10] = 17.6

HardAttack_F = dict()
HardAttack_F[1] = 0
HardAttack_F[2] = 0
HardAttack_F[3] = 0
HardAttack_F[4] = 0.5
HardAttack_F[5] = 1.5
HardAttack_F[6] = 2.3
HardAttack_F[7] = 3.4
HardAttack_F[8] = 6.8
HardAttack_F[9] = 13.5
HardAttack_F[10] = 27

################ DEFENSES & BREAKTHROUGHT
Defense_F = dict()
Defense_F[1] = 5
Defense_F[2] = 5.5
Defense_F[3] = 6.1
Defense_F[4] = 7.3
Defense_F[5] = 8.7
Defense_F[6] = 10.5
Defense_F[7] = 12.5
Defense_F[8] = 18.8
Defense_F[9] = 28.2
Defense_F[10] = 42.3

Breakthrought_F = dict()
Breakthrought_F[1] = 1
Breakthrought_F[2] = 1.1
Breakthrought_F[3] = 1.2
Breakthrought_F[4] = 1.5
Breakthrought_F[5] = 1.7
Breakthrought_F[6] = 2.1
Breakthrought_F[7] = 2.5
Breakthrought_F[8] = 3.8
Breakthrought_F[9] = 5.6
Breakthrought_F[10] = 8.5

################ BONUS OF PA
SoftAttack_PA = dict()
SoftAttack_PA[None] = 1
SoftAttack_PA[6] = 1.05
SoftAttack_PA[5] = 1.10
SoftAttack_PA[4] = 1.15
SoftAttack_PA[3] = 1.20
SoftAttack_PA[2] = 1.23
SoftAttack_PA[1] = 1.25

SoftAttack_CC_CT = dict()
SoftAttack_CC_CT[1] = 0.5
SoftAttack_CC_CT[2] = 0.8
SoftAttack_CC_CT[3] = 1.0
SoftAttack_CC_CT[4] = 1.2
SoftAttack_CC_CT[5] = 1.5
SoftAttack_CC_CT[6] = 1.8
SoftAttack_CC_CT[7] = 2.0
SoftAttack_CC_CT[8] = 2.5
SoftAttack_CC_CT[9] = 3.0

HardAttack_CC_CT = dict()
HardAttack_CC_CT[1] = 0.5
HardAttack_CC_CT[2] = 0.8
HardAttack_CC_CT[3] = 1.0
HardAttack_CC_CT[4] = 1.2
HardAttack_CC_CT[5] = 1.5
HardAttack_CC_CT[6] = 1.8
HardAttack_CC_CT[7] = 2.0
HardAttack_CC_CT[8] = 2.5
HardAttack_CC_CT[9] = 3.0

HardAttack_PA = dict()
HardAttack_PA[None] = 1
HardAttack_PA[6] = 1.01
HardAttack_PA[5] = 1.02
HardAttack_PA[4] = 1.05
HardAttack_PA[3] = 1.1
HardAttack_PA[2] = 1.25
HardAttack_PA[1] = 1.5

Defense_PA = dict()
Defense_PA[None] = 1
Defense_PA[6] = 1.05
Defense_PA[5] = 1.10
Defense_PA[4] = 1.15
Defense_PA[3] = 1.20
Defense_PA[2] = 1.25
Defense_PA[1] = 1.30

Breakthrought_PA = dict()
Breakthrought_PA[None] = 1
Breakthrought_PA[6] = 1.05
Breakthrought_PA[5] = 1.10
Breakthrought_PA[4] = 1.15
Breakthrought_PA[3] = 1.20
Breakthrought_PA[2] = 1.25
Breakthrought_PA[1] = 1.30

#################### HP Bonus Endurance
HPbonus_E = dict()
HPbonus_E[1] = 0.8
HPbonus_E[2] = 0.9
HPbonus_E[3] = 1.0
HPbonus_E[4] = 1.1
HPbonus_E[5] = 1.2
HPbonus_E[6] = 1.3
HPbonus_E[7] = 1.4
HPbonus_E[8] = 1.5
HPbonus_E[9] = 1.6
HPbonus_E[10] = 1.7

HMA_SMA_prop = dict()
"Proportion de HMA par rapport au SMA enf fonction de F"
HMA_SMA_prop[1] = 0
HMA_SMA_prop[2] = 0
HMA_SMA_prop[3] = 0.05
HMA_SMA_prop[4] = 0.1
HMA_SMA_prop[5] = 0.15
HMA_SMA_prop[6] = 0.20
HMA_SMA_prop[7] = 0.30
HMA_SMA_prop[8] = 0.50
HMA_SMA_prop[9] = 0.80
HMA_SMA_prop[10] = 1.5

Armor_SvgInvu = dict()
Armor_SvgInvu[2] = 1.5
Armor_SvgInvu[3] = 1.4
Armor_SvgInvu[4] = 1.3
Armor_SvgInvu[5] = 1.2
Armor_SvgInvu[6] = 1.1
Armor_SvgInvu[None] = 1
