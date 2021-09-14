#######################################################################################################################
# SOFT & HARD ATTACK
"""
Nombre de :SoftAttack: en fonction de la :Force: de l'unité
"""
SoftAttack_F = dict()
SoftAttack_F[1] = 0.15
SoftAttack_F[2] = 0.2
SoftAttack_F[3] = 0.27
SoftAttack_F[4] = 0.35
SoftAttack_F[5] = 0.47
SoftAttack_F[6] = 0.61
SoftAttack_F[7] = 0.73
SoftAttack_F[8] = 0.81
SoftAttack_F[9] = 0.85
SoftAttack_F[10] = 0.85
"""
Nombre de :HardAttack: en fonction de la :Force: de l'unité
"""
HardAttack_F = dict()
HardAttack_F[1] = 0
HardAttack_F[2] = 0
HardAttack_F[3] = 0
HardAttack_F[4] = 0.08
HardAttack_F[5] = 0.1
HardAttack_F[6] = 0.13
HardAttack_F[7] = 0.18
HardAttack_F[8] = 0.23
HardAttack_F[9] = 0.31
HardAttack_F[10] = 0.42

#######################################################################################################################
# SOFT & HARD MELEE ATTACK
"""
Nombre de :SoftMeleeAttack: en fonction de la :Force: de l'unité
"""
SoftMeleeAttack_F = dict()
SoftMeleeAttack_F[1] = 1
SoftMeleeAttack_F[2] = 1.1
SoftMeleeAttack_F[3] = 1.21
SoftMeleeAttack_F[4] = 1.33
SoftMeleeAttack_F[5] = 1.46
SoftMeleeAttack_F[6] = 1.54
SoftMeleeAttack_F[7] = 1.61
SoftMeleeAttack_F[8] = 1.69
SoftMeleeAttack_F[9] = 1.73
SoftMeleeAttack_F[10] = 1.76
"""
Nombre de :HardMeleeAttack: en fonction de la :Force: de l'unité
"""
HardMeleeAttack_F = dict()
HardMeleeAttack_F[1] = 0
HardMeleeAttack_F[2] = 0
HardMeleeAttack_F[3] = 0
HardMeleeAttack_F[4] = 0.05
HardMeleeAttack_F[5] = 0.15
HardMeleeAttack_F[6] = 0.23
HardMeleeAttack_F[7] = 0.34
HardMeleeAttack_F[8] = 0.68
HardMeleeAttack_F[9] = 1.35
HardMeleeAttack_F[10] = 2.7

################ DEFENSES & BREAKTHROUGHT
Defense_F = dict()
Defense_F[1] = 0.5
Defense_F[2] = 0.55
Defense_F[3] = 0.61
Defense_F[4] = 0.73
Defense_F[5] = 0.87
Defense_F[6] = 1.05
Defense_F[7] = 1.25
Defense_F[8] = 1.88
Defense_F[9] = 2.82
Defense_F[10] = 4.23

Breakthrought_F = dict()
Breakthrought_F[1] = 0.1
Breakthrought_F[2] = .11
Breakthrought_F[3] = .12
Breakthrought_F[4] = .15
Breakthrought_F[5] = .17
Breakthrought_F[6] = .21
Breakthrought_F[7] = .25
Breakthrought_F[8] = .38
Breakthrought_F[9] = .56
Breakthrought_F[10] = .85

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
HPbonus_E[1] = 0.4
HPbonus_E[2] = 0.7
HPbonus_E[3] = 1.0
HPbonus_E[4] = 1.5
HPbonus_E[5] = 2.3
HPbonus_E[6] = 3.4
HPbonus_E[7] = 5.1
HPbonus_E[8] = 7.6
HPbonus_E[9] = 11.4
HPbonus_E[10] = 17.1

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
