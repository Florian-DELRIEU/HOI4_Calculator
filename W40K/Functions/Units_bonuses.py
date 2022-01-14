def apply_SpecialRules(unit):
    """
    TODO
        - add bonus for "Immobile" rule
    """
    for rule in unit.SpecialRules:
        if rule == "Astartes":
            unit.ORG *= 1.2
        if rule == "Immobile":
            pass