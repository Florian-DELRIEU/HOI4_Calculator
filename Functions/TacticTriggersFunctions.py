def has_full_width(Battle,camp):
    return sum(division.width for division in camp.frontline) >= Battle.combat_width

def has_reserves_available(camp):
    return len(camp.reserves) > 0

def has_hardness_over(camp,hard_level):
    return any(division.hardness > hard_level for division in camp.frontline)

def has_river(Battle):
    return Battle.terrain.has_small_river or Battle.terrain.has_small_river