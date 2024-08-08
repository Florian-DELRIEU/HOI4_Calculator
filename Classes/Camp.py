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