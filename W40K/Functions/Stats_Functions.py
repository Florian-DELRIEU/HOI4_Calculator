import numpy as np
from MyPack2.Utilities import truncDecimal

########################################################################################################################
def setHP(object):
    if object.Class == "Infantry":      HP = object.PV * 1.5**(object.E-3)
    elif object.Class == "Vehicule":    HP = object.PC
    else:                       return AttributeError ,"object.Class not found"
    object.HP = HP/4
########################################################################################################################
def setORG(object):
    """
    FIXME
        - Revoir ci dessous
    """
    if object.Class == "Infantry":          ORG = object.Cd*10
    elif object.Class == "Vehicule":
        if "SuperHeavy" in object.Type:     ORG = 15
        elif "Artillerie" in object.Type:   ORG = 0
        elif "Walker" in object.Type :      ORG = 40
        else:                               ORG = 10
    else:                                   return AttributeError ,"object.Type not found"
    object.ORG = ORG
########################################################################################################################
def setSA(object):
    # sourcery skip: assign-if-exp, remove-unnecessary-else, swap-if-else-branches
    if object.Class == "Weapon":
        if object.Type == "Melee":          SA = 0
        else:                               SA = (np.arctan(object.F/0.5)**6)
        try:                                SA *= 1.2**(5-object.PA)
        except:                             pass
        SA *= object.Cadence
    else:                                   return AttributeError ,"object.Type not found"
    object.SoftAttack = truncDecimal(SA,2) /500
########################################################################################################################
def setHA(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, remove-unnecessary-else, swap-if-else-branches
    if object.Class == "Weapon":
        if object.Type == "Melee":          HA = 0
        elif object.F > 3:                  HA = np.exp(object.F/2)
        else:                               HA = 0
        try:                                HA *= ((1/object.PA**3)*216)**0.3
        except:                             pass
        HA *= object.Cadence
    else:                                   return AttributeError ,"object.Type not found"
    object.HardAttack = truncDecimal(HA,2) /3000
########################################################################################################################
def setSMA(object):  # sourcery skip: assign-if-exp, switch
    if object.Class == "Infantry":              SMA = (object.A/10)*1.3**(object.CC-3)
    elif object.Class == "Vehicule":
        if "Walker" in object.Type:             SMA = (object.A/10)*1.3**(object.CC-3)
        else:                                   SMA = 0
    elif object.Class == "Weapon":
        if object.Type == "Melee":          SMA = np.arctan(object.F/0.5)**6 /10
        else:                               SMA = 0
    elif object.Type == "Pistol":           SMA = 0.02
    else:                                   return AttributeError ,"object.Class not found"
    object.SoftMeleeAttack = SMA/10
########################################################################################################################
def setHMA(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, switch
    if object.Class == "Infantry" and object.F >= 4:
                                            HMA = object.SoftMeleeAttack*1.6**(object.F-4)
    elif object.Class == "Vehicule":
        if "Walker" in object.Type:         HMA = object.SoftMeleeAttack*1.6**(object.F-4)
        else:                               HMA = 0
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
    elif object.Class == "Vehicule":
        Armor = np.mean((object.Blind_Av, object.Blind_Side, object.Blind_Arr))
        if "Oppen-Topped" in object.SpecialRules: Armor /= 2
    else:                   return AttributeError ,"object.Class not found"
    object.Armor = Armor
########################################################################################################################
def setHardness(object):  # sourcery skip: remove-redundant-pass
# check class
    """
    FIXME
        - Detailler plus précisément les types de :param object: pour determiner l'Hardness
        - Revoir ci dessous
    """
    if object.Class == "Infantry":
        if object.Svg == 3:                         Hardness = 0.1
        elif object.Svg == 2:                       Hardness = 0.2
        else:                                       Hardness = 0

    elif object.Class == "Vehicule":
        Type = object.Type
        if Type == "Chariot":                       Hardness = 0.80
        elif Type == ("Tank" or ""):                Hardness = 0.90
        elif Type == "Heavy":                       Hardness = 0.95
        elif Type == "SuperHeavy":                  Hardness = 0.99

        elif Type == "Chariot SP Artillery":        Hardness = 0.50
        elif Type == ("Tank SP Artillery"
                      or "SP Artillery"):           Hardness = 0.65
        elif Type == "Heavy SP Artillery":          Hardness = 0.80
        elif Type == "SuperHeavy SP Artillery":     Hardness = 0.90

        elif Type == "Chariot Destroyer":           Hardness = 0.80
        elif Type == ("Tank Destroyer"
                      or "Destroyer"):              Hardness = 0.90
        elif Type == "Heavy Destroyer":             Hardness = 0.95
        elif Type == "SuperHeavy Destroyer":        Hardness = 0.99

        elif Type == "Walker":                      Hardness = 0.75
        else:                                       return AttributeError, "Tank Type not Found"

    else:                                           return AttributeError ,"object.Class not found"
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
        object.Piercing = PRC
    else:                       pass

########################################################################################################################
def setDefense(object):
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, switch
    """
    Pour chaques catégories la valeur dest divisé par le nombre d'unité dans une compangie (plus simple)
    afin de le rendre en accord avec les stats dans HOI IV
    """
    Class,Type = object.Class , object.Type
    if Class == "Vehicule":
        if Type == "Chariot":                       DEF = 4 / 15
        elif Type == ("Tank" or ""):                DEF = 5 / 15
        elif Type == "Heavy":                       DEF = 6 / 10
        elif Type == "SuperHeavy":                  DEF = 10 / 4
        
        elif   Type == "Chariot SP Artillery":      DEF = 4 / 15
        elif Type == ("Tank SP Artillery" 
                          or "SP Artillery"):       DEF = 5 / 15
        elif Type == "Heavy SP Artillery":          DEF = 6 / 10
        elif Type == "SuperHeavy SP Artillery":     DEF = 7 / 4
            
        elif   Type == "Chariot Destroyer":         DEF = 4 / 15
        elif Type == ("Tank Destroyer"
                   or "Destroyer"):                 DEF = 5 / 15
        elif Type == "Heavy Destroyer":             DEF = 6 / 10
        elif Type == "SuperHeavy Destroyer":        DEF = 7 / 4

        elif Type == "Walker":                      DEF = 10 / 15
        else:                                       return AttributeError, "Tank Type not Found"

    elif object.Class == "Infantry":        DEF = 20 / 100

    else:                               return AttributeError ,"object.Class not found"
    object.Defense = DEF
########################################################################################################################
def setBreakthrought(object):
    # sourcery skip: merge-duplicate-blocks, remove-pass-elif, remove-redundant-if, switch
    """
    Pour chaques catégories la valeur dest divisé par le nombre d'unité dans une compangie (plus simple)
    afin de le rendre en accord avec les stats dans HOI IV
    TODO
        - add Super heavy walker (Titan)
        - Heavy walker ??
    """
    Class, Type = object.Class, object.Type
    if object.Class == "Infantry":                BRK = 2 / 100
    elif Class == "Vehicule":

        if Type == "Chariot":                       BRK = 26 / 15
        elif Type == ("Tank" or ""):                BRK = 30 / 15
        elif Type == "Heavy":                       BRK = 40 / 10
        elif Type == "SuperHeavy":                  BRK = 70 / 4

        elif Type == "Chariot SP Artillery":        BRK = 2 / 15
        elif Type == ("Tank SP Artillery"
                      or "SP Artillery"):           BRK = 3 / 15
        elif Type == "Heavy SP Artillery":          BRK = 2 / 10
        elif Type == "SuperHeavy SP Artillery":     BRK = 3 /4

        elif Type == "Chariot Destroyer":           BRK = 1 / 15
        elif Type == ("Tank Destroyer"
                      or "Destroyer"):              BRK = 1.3 / 15
        elif Type == "Heavy Destroyer":             BRK = 1 / 10
        elif Type == "SuperHeavy Destroyer":        BRK = 4 / 4

        elif Type == "Walker":                      BRK = 12 / 15
        else:                                       return AttributeError, "Tank Type not Found"

    else:                               return AttributeError ,"object.Class not found"
    object.Breakthrought = BRK