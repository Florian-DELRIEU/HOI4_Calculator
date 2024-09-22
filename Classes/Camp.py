import random

class Camp:
    def __init__(self):
        self.divisions = []
        self.leader = None
        self.entrenchment = 0
        self.coordination = 0
        self.is_attacking = False
        self.frontline = []
        self.reserves = []
        self.tactic = None
        self.combat_penalty = 1
        self.battle_info = {}

    def __repr__(self):
        return "Camp Attacking" if self.is_attacking else "Camp Defending"
    ############# ROUNDS ####################

    def move_in_frontline(self):
        # Move divisions in frontline
        available_divisions = [division for division in self.divisions if
                               division not in self.frontline and division not in self.reserves]
        for division in available_divisions:
            width_filled = sum(division.width for division in self.frontline)
            total_battle_width = self.battle_info["Width"]
            if self.is_attacking: total_battle_width += (self.battle_info["extra side"]
                                                         *self.battle_info["terrain"].extra_width)
            if width_filled + division.width <= 1.33 * total_battle_width:
                self.frontline.append(division)

        # Move divisions in reserves
        for division in self.divisions:
            if division not in self.frontline:
                self.reserves.append(division)

        self.combat_width_penalty()

    def from_reserve_to_frontline(self):
        total_camp_width = sum(division.width for division in self.frontline)
        self.reserves.extend([division for division in self.divisions if division not in self.frontline
                                                                     and division not in self.reserves])
        for division in self.reserves:
            total_battle_width = self.battle_info["Width"]
            total_battle_width *= self.tactic.width_bonus
            if self.is_attacking: total_battle_width += (self.battle_info["extra side"]
                                                         * self.battle_info["terrain"].extra_width)
            if ((random.randint(0,100) <= 2 and total_camp_width + division.width <= 1.33 * total_battle_width)
                or len(self.frontline) == 0):
                self.frontline.append(self.reserves.pop(self.reserves.index(division)))
        self.combat_width_penalty()

    def combat_width_penalty(self):
        total_camp_width = sum(division.width for division in self.frontline)
        combat_width_malus = 1
        stacking_penalty = 1
        if total_camp_width >= self.battle_info["Width"]:
            combat_width_malus = min(total_camp_width / self.battle_info["Width"],1.33)
            #self.combat_width_malus = round(1 - (self.combat_width_malus-1),1)
        stacking_limit = 5 + 3 * self.battle_info["extra side"]
        if len(self.frontline) > stacking_limit:
            stacking_penalty = 2 * (len(self.frontline) - stacking_limit)
        self.combat_penalty = round(1 - (combat_width_malus+stacking_penalty - 2), 1)
        for division in self.frontline:
            division.combat_width_malus = self.combat_penalty

    ############# GESTION ####################
    def get_data(self):
        return {
            "divisions": [division.__dict__ for division in self.divisions],
            "leader": self.leader,
            "entrenchment": self.entrenchment,
        }

    def add_division(self, division):
        added_division = division.__copy__()
        added_division.camp_info = {
            "is_attacking": self.is_attacking,
            "coordination": self.coordination,
            "entrenchment_level": self.entrenchment,
            "leader": self.leader
        }
        self.divisions.append(added_division)

    def add_leader(self,leader):
        self.leader = leader
        if self.leader is not None: self.coordination = 0.01 + 0.02 * self.leader.level

    def remove_division(self, division_name):
        self.divisions = [d for d in self.divisions if d.template != division_name]

    def get_divisions(self):
        return self.divisions

    def contains_division(self, division):
        """
        Vérifie si une division donnée appartient à ce camp.
        """
        return any(division_in_camp.id == division.id for division_in_camp in self.divisions)

    def get_battle_info(self, Battle):
        self.battle_info["Width"] = Battle.combat_width
        self.battle_info["terrain"] = Battle.terrain
        self.battle_info["extra side"] = Battle.extra_side.get()
        self.battle_info["Fort Level"] = Battle.fort_level.get()