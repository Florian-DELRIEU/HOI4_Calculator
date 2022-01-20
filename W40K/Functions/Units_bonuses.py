def apply_SpecialRules(unit):  # sourcery skip: switch
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            unit.ORG *= 1.2
        if rule == "Oppen-Topped":
            unit.Hardness /= 2
        if rule == "Combat Squads":
            unit.Breaktrought *= 1.15
        if rule == "Combined Squads":
            unit.Defense *= 1.15
        if "Chapter:" in rule:
            apply_Faction(unit,rule.split(": ")[-1])

    if "Platform" in unit.Name:
        unit.Hardness = 0
        unit.Armor = 0
        unit.Type = "Platform"

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