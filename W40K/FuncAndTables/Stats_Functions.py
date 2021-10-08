from W40K.UnitCreator.Class.Unit import Infantry,Tank,Walker
from W40K.UnitCreator.Class.Weapons import Weapon
import numpy as np
########################################################################################################################
def setHP(object):
    if type(object) == Infantry:  HP = object.PV * 1.5**(object.E-3)
    elif type(object) == Tank:    HP = object.PC
    else:                       HP = None
    object.HP = HP
########################################################################################################################
def setORG(object):
    if type(object) == Infantry:
        ORG = object.Cd*10
    if type(object) == Tank:
        if object.Type == "SuperHeavy":     ORG = 15
        elif object.Type == "Artillerie":   ORG = 0
        else:                               ORG = 10
    if type(object) == Walker:              ORG = 40
    else:                                   ORG = None
    object.ORG = ORG
########################################################################################################################
def setSA(object):
    if type(object) == Weapon:
        if object.Type == "Melee":          SA = 0
        else:                               SA = (np.arctan(object.F/0.5)**6) * 1.2**(5-object.PA)
        SA *= object.Cadence
    else:                                   SA = None
    object.SoftAttack = SA
########################################################################################################################
def setHA(object):
    if type(object) == Weapon:
        if object.Type == "Melee":          HA = 0
        else:                               HA = np.exp(object.F/2)/10 * ((1/object.PA**3)*216)**0.3
        HA *= object.Cadence
    else:                                   HA = None
    object.HardAttack = HA
########################################################################################################################
def setSMA(object):
    if type(object) == Infantry:            SMA = (object.A/10)*1.3**(object.CC-3)
    elif type(object) == Tank:
        if object.Type == "Chariot":        SMA = 0.1
        elif object.Type == "Tank":         SMA = 0.3
        elif object.Type == "Heavy":        SMA = 0.5
        elif object.Type == "SuperHeavy":   SMA = 0.6
        elif object.Type == "Artillery":    SMA = 0
        else:                               SMA = None
    elif type(object) == Weapon:
        if object.Type == "Melee":          SMA = np.arctan(object.F/0.5)**6
        else:                               SMA = 0
    else:                                   SMA = None
    object.SoftMeleeAttack = SMA
########################################################################################################################
def setHMA(object):
    if type(object) == Infantry and object.F >= 3:
                                            HMA = object.SoftMeleeAttack*1.6**(object.F-4)
    elif type(object) == Tank:
        if object.Type == "Chariot":        HMA = 0
        elif object.Type == "Tank":         HMA = 0.1
        elif object.Type == "Heavy":        HMA = 0.2
        elif object.Type == "SuperHeavy":   HMA = 0.4
        elif object.Type == "Artillery":    HMA = 0
        else:                               HMA = None
    elif type(object) == Weapon:
        if object.Type == "Melee":          HMA = np.exp(object.F/2)/10
        else:                               HMA = 0
    else:                                   HMA = None
    object.HardMeleeAttack = HMA
########################################################################################################################
def setArmor(object):
    if type(object) == Infantry:
        if   object.Svg == 3:             Armor = 2
        elif object.Svg == 2:             Armor = 4
        else:                             Armor = 0
        if object.SvgInvu in [6,5,4,3,2]: Armor *= 1.15**(7-object.SvgInvu)
    elif type(object) == Tank or Walker:
        Armor = np.mean((object.Blind_Av, object.Blind_Side, object.Blind_Arr))
        if "Oppen-Topped" in object.SpecialRules: Armor /= 2
    else:                   Armor = None
    object.Armor = Armor
########################################################################################################################
def setHardness(object):
    if type(object) == Infantry:
        if object.Svg == 3:                         Hardness = 0.1
        elif object.Svg == 2:                       Hardness = 0.2
        else:                                       Hardness = 0
    if type(object) == Tank:
        if   object.Type == "Chariot":              Hardness = 0.80
        elif object.Type == "Tank":                 Hardness = 0.90
        elif object.Type == "Heavy":                Hardness = 0.95
        elif object.Type == "SuperHeavy":           Hardness = 0.99
        elif object.Type == "Artillery":            Hardness = 0
        else:                                       Hardness = None
        if "Oppen-Topped" in object.SpecialRules:   Hardness /= 2
        else:                                       Hardness = None
        if object.Hardness <= 0:                    Hardness = 0
        elif object.Hardness >= 1:                  Hardness = 1
        else:                                       Hardness = None
    if type(object) == Walker:                      Hardness = 0.7
    else:                                           Hardness = None
    object.Hardness = Hardness
########################################################################################################################
def setPiercing(object):
    PRC = object.F+4
    if type(object) == Weapon:
        if object.PA == 2:      PRC += 1
        elif object.PA == 1:    PRC += 2
        else:                   pass
    else:                       pass
    object.Piercing = PRC
########################################################################################################################
def setDefense(object):
    if type(object) == Weapon:
        DEF = 1.1**(object.F-3) * 1.1**(6-object.PA)
    elif type(object) == Infantry:
        DEF = 0.1* 1.1**(object.F - 3)
    else:
        DEF = None
    object.Defense = DEF
########################################################################################################################
def setBreakthrought(object):
    if type(object) == Weapon:
        BRK = 1.1**(object.F-3) * 1.1**(6-object.PA)
    elif type(object) == Infantry:
        BRK = 0.1* 1.1**(object.F - 3)
    else:
        BRK = None
    object.Breakthrought = BRK
########################################################################################################################