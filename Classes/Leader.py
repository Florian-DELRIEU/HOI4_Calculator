
class Leader:
    def __init__(self,name,atk_lvl=0,def_lvl=0,traits=dict):
        self.name = name
        self.attack_level = atk_lvl
        self.defense_level = def_lvl
        self.max_entrenchment_bonus = 0
        self.traits = traits
        self.level = self.attack_level + self.defense_level