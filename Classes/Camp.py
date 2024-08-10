class Camp:
    def __init__(self):
        self.divisions = []
        self.leader = ""
        self.entrenchment = 0.0
        self.coordination = 0
        self.is_attacking = False
        self.in_frontline = []
        self.in_reserves = []

    def get_data(self):
        return {
            "divisions": [division.__dict__ for division in self.divisions],
            "leader": self.leader,
            "entrenchment": self.entrenchment,
        }

    def add_division(self, division):
        self.divisions.append(division.__copy__())

    def remove_division(self, division_name):
        self.divisions = [d for d in self.divisions if d.template != division_name]

    def get_divisions(self):
        return self.divisions

    def do_attack(self):
        #todo Ajouter rafraichissement des valeurs de SA et HA en fonction de la strenght
        #   - Déplacer cette fonction vers les divisions ?
        #     pour avoir division.do_attack(target) ?
        for division in self.in_frontline:
            coordinated_share = 0.35 + self.coordination * (1 + division.initiative)
            sa_per_division = (division.soft_attack * (1 - coordinated_share)) // len(division.target_list)
            ha_per_division = (division.hard_attack * (1 - coordinated_share)) // len(division.target_list)
            sa_for_primary  = division.soft_attack * coordinated_share
            ha_for_primary  = division.hard_attack * coordinated_share
            for target in division.target_list:
                if target == division.primary_target:
                    total_sa = (sa_per_division + sa_for_primary) * (1 - target.hardness)
                    total_ha = (ha_per_division + ha_for_primary) * target.hardness
                else:
                    total_sa = sa_per_division * (1 - target.hardness)
                    total_ha = ha_per_division * target.hardness
                total_attack = total_sa + total_ha
                total_attack = total_attack if division.piercing >= target.armor else total_attack/2
                total_attack /= 10
