import numpy as np
from MyPack.Utilities import truncDecimal
########################################################################################################################
def setHP(object):
    if object.Class == "Infantry":  HP = object.PV * 1.5**(object.E-3)
    elif object.Class == "Tank":    HP = object.PC
    else:                       return AttributeError ,"object.Class not found"
    object.HP = HP
########################################################################################################################
def setORG(object):
    if object.Class == "Infantry":
        ORG = object.Cd*10
    if object.Class == "Tank":
        if object.Type == "SuperHeavy":     ORG = 15
        elif object.Type == "Artillerie":   ORG = 0
        else:                               ORG = 10
    if object.Class == "Walker":            ORG = 40
    else:                                   return AttributeError ,"object.Type not found"
    object.ORG = ORG
########################################################################################################################
def setSA(object):
    if object.Class == "Weapon":
        if object.Type == "Melee":          SA = 0
        else:                               SA = (np.arctan(object.F/0.5)**6)
        try:                                SA *= 1.2**(5-object.PA)
        except:                             pass
        SA *= object.Cadence
    else:                                   return AttributeError ,"object.Type not found"
    object.SoftAttack = truncDecimal(SA,2)
########################################################################################################################
def setHA(object):
    if object.Class == "Weapon":
        if object.Type == "Melee":          HA = 0
        elif object.F > 3:                  HA = np.exp(object.F/2)/10
        else:                               HA = 0
        try:                                HA *= ((1/object.PA**3)*216)**0.3
        except:                             pass
        HA *= object.Cadence
    else:                                   return AttributeError ,"object.Type not found"
    object.HardAttack = HA
########################################################################################################################
def setSMA(object):
    if object.Class == "Infantry":            SMA = (object.A/10)*1.3**(object.CC-3)
    elif object.Class == "Tank":
        if object.Type == "Chariot":        SMA = 0.1
        elif object.Type == "Tank":         SMA = 0.3
        elif object.Type == "Heavy":        SMA = 0.5
        elif object.Type == "SuperHeavy":   SMA = 0.6
        elif object.Type == "Artillery":    SMA = 0
        else:                               return AttributeError ,"object.Type not found"
    elif object.Class == "Weapon":
        if object.Type == "Melee":          SMA = np.arctan(object.F/0.5)**6
        else:                               SMA = 0
    else:                                   return AttributeError ,"object.Class not found"
    object.SoftMeleeAttack = SMA
########################################################################################################################
def setHMA(object):
    if object.Class == "Infantry" and object.F >= 3:
                                            HMA = object.SoftMeleeAttack*1.6**(object.F-4)
    elif object.Class == "Tank":
        if object.Type == "Chariot":        HMA = 0
        elif object.Type == "Tank":         HMA = 0.1
        elif object.Type == "Heavy":        HMA = 0.2
        elif object.Type == "SuperHeavy":   HMA = 0.4
        elif object.Type == "Artillery":    HMA = 0
        else:                               return AttributeError ,"object.Type not found"
    elif object.Class == "Weapon":
        if object.Type == "Melee":          HMA = np.exp(object.F/2)/10
        else:                               HMA = 0
    else:                                   return AttributeError ,"object.Class not found"
    object.HardMeleeAttack = HMA
########################################################################################################################
def setArmor(object):
    if object.Class == "Infantry":
        if   object.Svg == 3:             Armor = 2
        elif object.Svg == 2:             Armor = 4
        else:                             Armor = 0
        if object.SvgInvu in [6,5,4,3,2]: Armor *= 1.15**(7-object.SvgInvu)
    elif object.Class == "Tank" or "Walker":
        Armor = np.mean((object.Blind_Av, object.Blind_Side, object.Blind_Arr))
        if "Oppen-Topped" in object.SpecialRules: Armor /= 2
    else:                   return AttributeError ,"object.Class not found"
    object.Armor = Armor
########################################################################################################################
def setHardness(object):
# check class
    if object.Class == "Infantry":
        if object.Svg == 3:                         Hardness = 0.1
        elif object.Svg == 2:                       Hardness = 0.2
        else:                                       Hardness = 0
    elif object.Class == "Tank":
        if   object.Type == "Chariot":              Hardness = 0.80
        elif object.Type == "Tank":                 Hardness = 0.90
        elif object.Type == "Heavy":                Hardness = 0.95
        elif object.Type == "SuperHeavy":           Hardness = 0.99
        elif object.Type == "Artillery":            Hardness = 0
        else:                                       return AttributeError ,"object.Type not found"
    elif object.Class == "Walker":                  Hardness = 0.7
    else:                                           return AttributeError ,"object.Class not found"
# check rules
    if "Oppen-Topped" in object.SpecialRules:   Hardness /= 2
    else:                                       pass
# check hardness out of bounds
    if object.Hardness <= 0:                    Hardness = 0
    elif object.Hardness >= 1:                  Hardness = 1
    else:                                       pass
    object.Hardness = Hardness
########################################################################################################################
def setPiercing(object):
    if object.Class == "Weapon":
        PRC = object.F+4
        if object.PA == 2:      PRC += 1
        elif object.PA == 1:    PRC += 2
        else:                   pass
    else:                       PRC = 0
    object.Piercing = PRC
########################################################################################################################
def setDefense(object):
    if object.Class == "Weapon":
        DEF = 1.1**(object.F-3)
        try:    DEF *= 1.1**(6-object.PA)
        except: pass
    elif object.Class == "Infantry":
        DEF = 0.1* 1.1**(object.F - 3)
    else:
        return AttributeError ,"object.Class not found"
    object.Defense = DEF
########################################################################################################################
def setBreakthrought(object):
    if object.Class == "Weapon":
        BRK = 1.1**(object.F-3)
        try:    BRK *= 1.1**(6-object.PA)
        except: pass
    elif object.Class == "Infantry":
        BRK = 0.1* 1.1**(object.F - 3)
    else:
        return AttributeError ,"object.Class not found"
    object.Breakthrought = BRK
########################################################################################################################