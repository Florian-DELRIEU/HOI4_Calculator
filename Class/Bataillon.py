class Bataillon:
    def __init__(self, pv, org, sa, ha, defense, attack, armor, prc, hard, width, supply_use=None, fuel_use=None, ic=None, name=""):
        self.pv = pv
        self.org = org
        self.sa = sa
        self.ha = ha
        self.defense = defense
        self.attack = attack
        self.armor = armor
        self.prc = prc
        self.hard = hard
        self.width = width
        self.supply_use = supply_use
        self.fuel_use = fuel_use
        self.ic = ic
        self.name = name

    def __repr__(self):
        return self.name
