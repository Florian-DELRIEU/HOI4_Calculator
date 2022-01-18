def apply_SpecialRules(company):  # sourcery skip: switch
    unit = company.Unit
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            company.ORG *= 1.2
        if rule == "Immobile":
            company.Hardness = 0
        if rule == "Oppen-Topped":
            company.Harness /= 2
        if rule == "Combat Squads":
            company.Breaktrought *= 1.15
        if rule == "Heavy Weapons Team":
            for weapon in company.Equipement:
                if weapon.Type == "Lourde":
                    weapon.Breakthrought_bonus += 0.1
        if rule == "Combined Squads":
            company.Defense *= 1.15
        if "Chapter:" in rule:
            apply_Faction(unit,rule.split(": ")[-1])

def apply_Vehicule(vehicule):  # sourcery skip: remove-pass-elif
    Class,Type = vehicule.Class, vehicule.Type
    if Class == "Vehicule":

        if Type == "Chariot":
            vehicule.SoftAttack *= 2
            vehicule.HardAttack *= 2
        elif Type == ("Tank" or ""):
            vehicule.SoftAttack *= 3
            vehicule.HardAttack *= 3
        elif Type == "Heavy":
            vehicule.SoftAttack *= 5
            vehicule.HardAttack *= 5
        elif Type == "SuperHeavy":
            vehicule.SoftAttack *= 7
            vehicule.HardAttack *= 7

        elif Type == "Chariot SP Artillery":
            vehicule.SoftAttack *= 15
            vehicule.HardAttack *= 1
        elif Type == ("Tank SP Artillery"
                      or "SP Artillery"):
            vehicule.SoftAttack *= 20
            vehicule.HardAttack *= 1
        elif Type == "Heavy SP Artillery":
            vehicule.SoftAttack *= 25
            vehicule.HardAttack *= 1
        elif Type == "SuperHeavy SP Artillery":
            vehicule.SoftAttack *= 30
            vehicule.HardAttack *= 3

        elif Type == "Chariot Destroyer":
            vehicule.SoftAttack *= 1
            vehicule.HardAttack *= 7
        elif Type == ("Tank Destroyer"
                      or "Destroyer"):
            vehicule.SoftAttack *= 1
            vehicule.HardAttack *= 10
        elif Type == "Heavy Destroyer":
            vehicule.SoftAttack *= 1
            vehicule.HardAttack *= 13
        elif Type == "SuperHeavy Destroyer":
            vehicule.SoftAttack *= 1
            vehicule.HardAttack *= 16

        elif Type == "Walker":pass
        else:                                       return AttributeError, "Tank Type not Found"

def apply_Faction(unit,rule):
    """
    FIXME
        - Voir si je change les poids de certaines tactiques pour "ULTRAMARINES"
    """
    if rule == "Ultramarines":
        unit.SoftAttack *= 1.05
        unit.HardAttack *= 1.05