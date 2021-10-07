from W40K.UnitCreator.Class.Unit import Infantry,Tank,Walker
import numpy as np

def setHP(unit):
    if type(unit) == Infantry:  HP = unit.PV * 1.5**(unit.E-3)
    elif type(unit) == Tank:    HP = unit.PC
    else:                       HP = None
    unit.HP = HP

def setORG(unit):
    if type(unit) == Infantry:
        ORG = unit.Cd*10
    if type(unit) == Tank:
        if unit.Type == "SuperHeavy":   ORG = 15
        elif unit.Type == "Artillerie": ORG = 0
        else:                           ORG = 10
    if type(unit) == Walker:            ORG = 10
    else:                               ORG = None
    unit.ORG = ORG

def setSMA(unit):
    if type(unit) == Infantry:
        SMA = (unit.A / 10) * 1.3**(unit.CC-3)
    if type(unit) == Tank and unit.Type == "Chariot":     SMA = 0.1
    elif type(unit) == Tank and unit.Type == "Tank":      SMA = 0.3
    elif type(unit) == Tank and unit.Type == "Heavy":     SMA = 0.5
    elif type(unit) == Tank and unit.Type == "SuperHeavy":SMA = 0.6
    elif type(unit) == Tank and unit.Type == "Artillery": SMA = 0
    else:                                                 SMA = None
    unit.SoftMeleeAttack = SMA

def setHMA(unit):
    if type(unit) == Infantry and unit.F >= 3:
        HMA = unit.SoftMeleeAttack * 1.6**(unit.F-4)
    if type(unit) == Tank and unit.Type == "Chariot":     HMA = 0
    elif type(unit) == Tank and unit.Type == "Tank":      HMA = 0.1
    elif type(unit) == Tank and unit.Type == "Heavy":     HMA = 0.2
    elif type(unit) == Tank and unit.Type == "SuperHeavy":HMA = 0.4
    elif type(unit) == Tank and unit.Type == "Artillery": HMA = 0
    else:                                                 HMA = 0
    unit.HardMeleeAttack = HMA

def setArmor(unit):
    if type(unit) == Infantry:
        if   unit.Svg == 3:             Armor = 2
        elif unit.Svg == 2:             Armor = 4
        else:                           Armor = 0
        if unit.SvgInvu in [6,5,4,3,2]: Armor *= 1.15**(7-unit.SvgInvu)
    elif type(unit) == Tank or Walker:
        Armor = np.mean((unit.Blind_Av, unit.Blind_Side, unit.Blind_Arr))
        if "Oppen-Topped" in unit.SpecialRules: Armor /= 2
    else:                   Armor = None
    unit.Armor = Armor


def setHardness(unit):
    if type(unit) == Infantry:
        if unit.Svg == 3:               Hardness = 0.1
        elif unit.Svg == 2:             Hardness = 0.2
        else:                           Hardness = 0
    if type(unit) == Tank:
        if   unit.Type == "Chariot":    Hardness = 0.80
        elif unit.Type == "Tank":       Hardness = 0.90
        elif unit.Type == "Heavy":      Hardness = 0.95
        elif unit.Type == "SuperHeavy": Hardness = 0.99
        elif unit.Type == "Artillery":  Hardness = 0
        else:                           Hardness = None
        if "Oppen-Topped" in unit.SpecialRules: Hardness /= 2
        if unit.Hardness <= 0:          Hardness = 0
        if unit.Hardness >= 1:          Hardness = 1
    if type(unit) == Walker:            Hardness = 0.7
    else:                               Hardness = None
    unit.Hardness = Hardness

def setPiercing(unit):
    PRC = unit.F+4
    unit.Piercing = PRC

def setDefense(unit):
    pass

def setBreakthrought(unit):
    pass