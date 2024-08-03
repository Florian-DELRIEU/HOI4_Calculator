import string
import random



class Camp:
    def __init__(self):
        self.divisions = []
        self.leader = ""
        self.entrenchment = 0.0

    def add_division(self, division):
        self.divisions.append(division)

    def remove_division(self, division_name):
        self.divisions = [d for d in self.divisions if d.template != division_name]
    def get_divisions(self):
        return self.divisions


class Division:
    def __init__(self, template, pv, organisation, soft_attack, hard_attack, defense, attaque, piercing, armor, hardness, width):
        self.nom = ""
        self.template = template
        self._pv = pv
        self._organisation = organisation
        self.pv = self._pv
        self.organisation = self._organisation
        self.soft_attack = soft_attack
        self.hard_attack = hard_attack
        self.defense = defense
        self.attaque = attaque
        self.piercing = piercing
        self.armor = armor
        self.hardness = hardness
        self.width = width
        self.id = self.generate_id()

    def generate_id(self,length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def save(self):
        return {
            "Nom de Template": self.template,
            "PV": self.pv,
            "Organisation": self.organisation,
            "Soft Attack": self.soft_attack,
            "Hard Attack": self.hard_attack,
            "Defense": self.defense,
            "Attaque": self.attaque,
            "Piercing": self.piercing,
            "Armor": self.armor,
            "Hardness": self.hardness,
            "Width": self.width,
        }

    @staticmethod
    def load(data):
        return Division(
            data["Nom de Template"], data["PV"], data["Organisation"], data["Soft Attack"], data["Hard Attack"],
            data["Defense"], data["Attaque"], data["Piercing"], data["Armor"], data["Hardness"], data["Width"]
        )
