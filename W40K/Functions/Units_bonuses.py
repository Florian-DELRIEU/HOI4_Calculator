def setUnitBonus(unit):
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            unit.ORG *= 1.2
        elif rule == "Immobile":
            unit.Breaktrought = 0
            unit.Defense *= 1.2