class Division:
    def __init__(self, nom, pv, organisation, soft_attack, hard_attack, defense, attaque, piercing, armor, hardness, entrenchment, width):
        self.nom = nom
        self.pv = pv
        self.organisation = organisation
        self.soft_attack = soft_attack
        self.hard_attack = hard_attack
        self.defense = defense
        self.attaque = attaque
        self.piercing = piercing
        self.armor = armor
        self.hardness = hardness
        self.entrenchment = entrenchment
        self.width = width

    def to_dict(self):
        return {
            "Nom de la division": self.nom,
            "PV": self.pv,
            "Organisation": self.organisation,
            "Soft Attack": self.soft_attack,
            "Hard Attack": self.hard_attack,
            "Defense": self.defense,
            "Attaque": self.attaque,
            "Piercing": self.piercing,
            "Armor": self.armor,
            "Hardness": self.hardness,
            "Entrenchment": self.entrenchment,
            "Width": self.width,
        }

    @staticmethod
    def from_dict(data):
        return Division(
            data["Nom de la division"], data["PV"], data["Organisation"], data["Soft Attack"], data["Hard Attack"],
            data["Defense"], data["Attaque"], data["Piercing"], data["Armor"], data["Hardness"], data["Entrenchment"], data["Width"]
        )
