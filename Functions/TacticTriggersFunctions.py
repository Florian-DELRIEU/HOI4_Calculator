def has_full_width(Battle,camp):
    return sum(division.width for division in camp.frontline) >= Battle.combat_width

def has_reserves_available(camp):
    return len(camp.reserves) > 0