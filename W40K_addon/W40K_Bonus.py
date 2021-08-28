from W40K_addon.W40K_Company import *

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
    if Object.Range == (0 or None): pass
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

def setUpgradeBonus(company):
    #assert type(company) is Company, "Argument must be a company"
    SoftAttack_Bonus = 1
    HardAttack_Bonus = 1
    SoftMeleeAttack_Bonus = 1
    HardMeleeAttack_Bonus = 1
    Defense_Bonus = 1
    Breakthrought_Bonus = 1
    for el in company.Upgrade: # Additionne tout les bonus des Upgrades
        equip_ratio = el.Quantity/company.Manpower
    # Cette opération est pour incorporer le :equip_ratio: dans les bonus
        SoftAttack_Bonus *= 1 + (el.SoftAttack_Bonus-1)*equip_ratio
        HardAttack_Bonus *= 1 + (el.HardAttack_Bonus-1)*equip_ratio
        SoftMeleeAttack_Bonus *= 1 + (el.SoftMeleeAttack_Bonus-1)*equip_ratio
        HardMeleeAttack_Bonus *= 1 + (el.HardMeleeAttack_Bonus-1)*equip_ratio
        Defense_Bonus *= 1 + (el.Defense_Bonus-1)*equip_ratio
        Breakthrought_Bonus *= 1 + (el.Breakthrought_Bonus-1)*equip_ratio
    company.SoftAttack = company.SoftAttack*SoftAttack_Bonus
    company.HardAttack = company.HardAttack*HardAttack_Bonus
    company.SoftMeleeAttack = company.SoftMeleeAttack*SoftMeleeAttack_Bonus
    company.HardMeleeAttack = company.HardMeleeAttack*HardMeleeAttack_Bonus
    company.Defense = company.Defense*Defense_Bonus
    company.Breakthrought = company.Breakthrought*Breakthrought_Bonus