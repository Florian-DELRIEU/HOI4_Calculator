import numpy as np
from MyPack2.Utilities import truncDecimal

########################################################################################################################
def setHP(object):
    if object.Class == "Infantry":  HP = object.PV * 1.5**(object.E-3)
    elif object.Class == "Tank":    HP = object.PC
    else:                       return AttributeError ,"object.Class not found"
    object.HP = HP/4
########################################################################################################################
def setORG(object):
    if object.Class == "Infantry":
        ORG = object.Cd*10
    elif object.Class == "Tank":
        if object.Type == "SuperHeavy":     ORG = 15
        elif object.Type == "Artillerie":   ORG = 0
        else:                               ORG = 10
    elif object.Class == "Walker":            ORG = 40
    else:                                   return AttributeError ,"object.Type not found"
    object.ORG = ORG
########################################################################################################################
def setSA(object):
    # sourcery skip: assign-if-exp, remove-unnecessary-else, swap-if-else-branches
    if object.Class == "Weapon":
        if object.Type == "Melee":          SA = 0
        else:                               SA = (np.arctan(object.F/0.5)**6) /10
        try:                                SA *= 1.2**(5-object.PA)
        except:                             pass
        SA *= object.Cadence
    else:                                   return AttributeError ,"object.Type not found"
    object.SoftAttack = truncDecimal(SA,2)/10
########################################################################################################################
def setHA(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, remove-unnecessary-else, swap-if-else-branches
    if object.Class == "Weapon":
        if object.Type == "Melee":          HA = 0
        elif object.F > 3:                  HA = np.exp(object.F/2) /100
        else:                               HA = 0
        try:                                HA *= ((1/object.PA**3)*216)**0.3
        except:                             pass
        HA *= object.Cadence
    else:                                   return AttributeError ,"object.Type not found"
    object.HardAttack = HA/10
########################################################################################################################
def setSMA(object):  # sourcery skip: assign-if-exp, switch
    if object.Class == "Infantry":            SMA = (object.A/10)*1.3**(object.CC-3)
    elif object.Class == "Tank":
        if object.Type == "Chariot":        SMA = 0.1
        elif object.Type == "Tank":         SMA = 0.3
        elif object.Type == "Heavy":        SMA = 0.5
        elif object.Type == "SuperHeavy":   SMA = 0.6
        elif object.Type == "Artillery":    SMA = 0
        else:                               return AttributeError ,"object.Type not found"
    elif object.Class == "Weapon":
        if object.Type == "Melee":          SMA = np.arctan(object.F/0.5)**6 /10
        else:                               SMA = 0
    else:                                   return AttributeError ,"object.Class not found"
    object.SoftMeleeAttack = SMA/10
########################################################################################################################
def setHMA(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, switch
    if object.Class == "Infantry" and object.F >= 4:
                                            HMA = object.SoftMeleeAttack*1.6**(object.F-4)
    elif object.Class == "Tank":
        if object.Type == "Chariot":        HMA = 0
        elif object.Type == "Tank":         HMA = 0.1
        elif object.Type == "Heavy":        HMA = 0.2
        elif object.Type == "SuperHeavy":   HMA = 0.4
        elif object.Type == "Artillery":    HMA = 0
        else:                               return AttributeError ,"object.Type not found"
    elif object.Class == "Weapon" and object.F >= 4:
        if object.Type == "Melee":          HMA = np.exp(object.F/2) /100
        elif "Krak Grenade" in object.SpecialsRules:
                                            HMA = np.exp(object.F/2)/100
        else:                               HMA = 0
    else:                                   return AttributeError ,"object.Class not found"
    object.HardMeleeAttack = HMA/10
########################################################################################################################
def setArmor(object):  # sourcery skip: remove-redundant-if
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
def setHardness(object):  # sourcery skip: remove-redundant-pass
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
    if "Oppen-Topped" in object.SpecialRules:       Hardness /= 2
    else:                                           pass
# check hardness out of bounds
    if Hardness <= 0:                               Hardness = 0
    elif Hardness >= 1:                             Hardness = 1
    else:                                           pass
    object.Hardness = Hardness
########################################################################################################################
def setPiercing(object):  # sourcery skip: remove-redundant-pass, switch
    if object.Class == "Weapon":
        PRC = object.F+4
        if object.PA == 2:      PRC += 1
        elif object.PA == 1:    PRC += 2
        else:                   pass
    else:                       PRC = 0
    object.Piercing = PRC
########################################################################################################################
def setDefense(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, switch
    """
    BRK of an weapons regarding this F and E
    """
    if object.Class == "Weapon":        DEF = 0.1
    elif object.Class == "Tank":        DEF = 1
    elif object.Class == "Infantry":    DEF = 1
    else:                               return AttributeError ,"object.Class not found"
    object.Defense = DEF
########################################################################################################################
def setBreakthrought(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, switch
    """
    BRK of an weapons regarding this F and E

    TODO
        - add bonus for Company
    """
    if object.Class == "Weapon":        BRK = 0.1
    elif object.Class == "Tank":        BRK = 1
    elif object.Class == "Infantry":    BRK = 1
    else:                               return AttributeError ,"object.Class not found"
    object.Breakthrought = BRK