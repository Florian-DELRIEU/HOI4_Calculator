def apply_SpecialRules(unit):
    """
    TODO
        - add bonus for "Immobile" rule
    """
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            unit.ORG *= 1.2

def apply_Vehicule(vehicule):
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

        elif Type != "Walker":                                       return AttributeError, "Tank Type not Found"