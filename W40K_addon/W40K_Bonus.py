from W40K_Unit import *
from W40K_Weapons import *

def setWeaponsBonus(Object):
# Weapons Specials rules
    for rule in Object.SpecialsRules:
        if rule == "Perforant":
            Object.SoftAttack *= 1.1
            Object.HardAttack *= 1.1
            Object.Piercing += 1
        if rule == "Fléau de la chair":
            Object.SoftAttack *= 1.1
        if rule == "Fléau des chars":
            Object.HardAttack *= 1.1
        if rule == "Ignore les couverts":
            Object.SoftAttack *= 1.2
        if rule == "Blast 3'":
            Object.SoftAttack *= 1.1
            Object.HardAttack += 1.02
        if rule == "Blast 5'":
            Object.SoftAttack *= 1.2
            Object.HardAttack += 1.05
# Weapons type
    if Object.Type == "Lourde":
        Object.Defense *= 1.2
    if Object.Type == "Assaut":
        Object.Breakthrought *= 1.2
    if Object.Type == "Tir Rapide": pass
    if Object.Type == "Salve":
        Object.Defense *= 1.1
        Object.Breakthrought = 1.1
# Weapon Range
    if Object.Range <= 8:
        Object.SoftAttack *= 0.4
        Object.HardAttack *= 0.4
        Object.Defense *= 0.4
        Object.Breakthrought *= 0.4
    elif Object.Range <= 12:
        Object.SoftAttack *= 0.6
        Object.HardAttack *= 0.6
        Object.Defense *= 0.6
        Object.Breakthrought *= 0.6
    elif Object.Range <= 18:
        Object.SoftAttack *= 0.8
        Object.HardAttack *= 0.8
        Object.Defense *= 0.8
        Object.Breakthrought *= 0.8
    elif Object.Range >= 30:
        Object.SoftAttack *= 1.2
        Object.HardAttack *= 1.2
        Object.Defense *= 1.2
        Object.Breakthrought *= 1.2

def setUpgradeBonus(Company):
    assert type(Company) is Company , "Argument must be a company"
    SoftAttack_Bonus = 1
    HardAttack_Bonus = 1
    SoftMeleeAttack_Bonus = 1
    HardMeleeAttack_Bonus = 1
    Defense_Bonus = 1
    Breakthrought_Bonus = 1
    for el in Company.Upgrade: # Additionne tout les bonus des Upgrades
        SoftAttack_Bonus += el.SoftAttack_Bonus
        HardAttack_Bonus += el.HardAttack_Bonus
        SoftMeleeAttack_Bonus += el.SoftMeleeAttack_Bonus
        HardMeleeAttack_Bonus += el.HardMeleeAttack_Bonus
        Defense_Bonus += el.Defense_Bonus
        Breakthrought_Bonus += el.Breakthrought_Bonus
    Company.SoftAttack = Company.SoftAttack * SoftAttack_Bonus
    Company.HardAttack = Company.HardAttack * HardAttack_Bonus
    Company.SoftMeleeAttack = Company.SoftMeleeAttack * SoftMeleeAttack_Bonus
    Company.HardMeleeAttack = Company.HardMeleeAttack * HardMeleeAttack_Bonus
    Company.Defense = Company.Defense * Defense_Bonus
    Company.Breakthrought = Company.Breakthrought * Breakthrought_Bonus
