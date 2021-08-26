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