def setUnitBonus(unit):
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            unit.ORG *= 1.2