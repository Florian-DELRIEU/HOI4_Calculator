import string
import random

class Division:
    def __init__(self, template, pv, organisation, soft_attack, hard_attack, defense, attaque, piercing, armor,
                 hardness, width, initiative):
        self.nom = ""
        self.template = template
        self._PV = pv
        self._ORGANISATION = organisation
        self._DEFENSE = defense
        self._ATTAQUE = attaque
        self._SOFT_ATTACK = soft_attack
        self._HARD_ATTACK = hard_attack
        self.pv = pv
        self.organisation = organisation
        self.soft_attack = soft_attack
        self.hard_attack = hard_attack
        self.attaque = attaque
        self.defense = defense
        self.piercing = piercing
        self.armor = armor
        self.hardness = hardness
        self.width = width
        self.initiative = initiative
        self.id = self.generate_id()
        self.target_list = []
        self.primary_target = None

    def generate_id(self,length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def save(self):
        return {
            "Nom de Template": self.template,
            "PV": self._PV,
            "Organisation": self._ORGANISATION,
            "Soft Attack": self._SOFT_ATTACK,
            "Hard Attack": self._HARD_ATTACK,
            "Defense": self._DEFENSE,
            "Attaque": self._ATTAQUE,
            "Piercing": self.piercing,
            "Armor": self.armor,
            "Hardness": self.hardness,
            "Width": self.width,
            "Initiative": self.initiative,
        }

    def __copy__(self):
        """
        Programme permmettant de copier un object quelconque
          - Attention : newObject = Object_a_copier()
        """
        newObject = Division(0,0,0,0,0,0,0,0,0,0,0,0)
        for attr in self.__dict__:
            newObject.__setattr__(attr,self.__getattribute__(attr))
        return newObject

    @staticmethod
    def load(data):
        return Division(
            data["Nom de Template"], data["PV"], data["Organisation"], data["Soft Attack"], data["Hard Attack"],
            data["Defense"], data["Attaque"], data["Piercing"], data["Armor"], data["Hardness"], data["Width"],
            data["Initiative"]
        )

    def choose_priority_target(self):
        """
        Définie la cible prioritaire en fonction des paramètres
        :param attacking_division:
        :param target_list:
        :return:
        """
        def target_priority(target):
            """
            Calcul le score de priorisation des cibles
            :param target:
            :return: La cible avec le plus grand score devient la cible prioritaire
            """
            effective_attacks = self.hard_attack if target.hardness > 0.5 else self.soft_attack
            if target.armor > self.piercing:
                effective_attacks /= 2
            priority_score = effective_attacks * (1 - target.organisation / 400)
            return priority_score

        priority_scores_dict = {}
        for division in self.target_list:
            priority_scores_dict[division] = target_priority(division)

        self.primary_target = max(priority_scores_dict, key=priority_scores_dict.get)


