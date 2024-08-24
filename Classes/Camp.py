import random

class Camp:
    def __init__(self):
        self.divisions = []
        self.leader = ""
        self.entrenchment = 0.0
        self.coordination = 0
        self.is_attacking = False
        self.frontline = []
        self.reserves = []

        self.battle_info = {}

    def __repr__(self):
        return "Camp Attacking" if self.is_attacking else "Camp Defending"
    ############# ROUNDS ####################

    def move_in_frontline(self):
        # Move divisions in frontline
        available_divisions = [division for division in self.divisions if
                               division not in self.frontline and division not in self.reserves]
        for division in available_divisions:
            total_camp_width = sum(division.width for division in self.frontline)
            if total_camp_width + division.width <= self.battle_info["Width"]:
                self.frontline.append(division)
        # Move divisions in reserves
        for division in self.divisions:
            if division not in self.frontline:
                self.reserves.append(division)

    def from_reserve_to_frontline(self):
        for division in self.reserves:
            if random.randint(0,100) <= 2:
                self.frontline.append(self.reserves.pop(self.reserves.index(division)))


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
            "coordination": self.coordination
        }
        self.divisions.append(added_division)


    def remove_division(self, division_name):
        self.divisions = [d for d in self.divisions if d.template != division_name]

    def get_divisions(self):
        return self.divisions

    def contains_division(self, division):
        """
        Vérifie si une division donnée appartient à ce camp.
        """
        return any(division_in_camp.id == division.id for division_in_camp in self.divisions)


    def get_battle_info(self,battle_window):
        self.battle_info["Width"] = battle_window.terrain.width
