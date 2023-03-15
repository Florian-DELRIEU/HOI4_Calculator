

class Tactic:
    def __init__(self, attacker_damage=1, attacker_defense=1, defender_damage=1, defender_defense=1, weight=4, countered_by=None, name="",
                 BeginPhase=None):
        self.name = name
        self.countered_by = countered_by
    # Bonus
        self.attacker_damage = attacker_damage
        self.attacker_defense = attacker_defense
        self.defender_damage = defender_damage
        self.defender_defense = defender_defense
    # Begin battle phase
        self.weight = weight
        self.begin_battle_phase = None

    def __repr__(self):
        return self.name
    