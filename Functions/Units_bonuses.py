def apply_SpecialRules(unit):
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            unit.org *= 1.2
        elif rule == "Immobile":
            unit.Breaktrought = 0 if unit.Type != "Artillery" else 0.8
            unit.Defense *= 1.2