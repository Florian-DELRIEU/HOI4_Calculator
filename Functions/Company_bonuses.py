def apply_SpecialRules(company):  # sourcery skip: switch
    unit = company.Unit
    for rule in unit.SpecialRules:
        if rule == "Heavy Weapons Team":
            for weapon in company.Equipement:
                if weapon.Type == "Lourde":
                    weapon.Breakthrought_bonus = 0