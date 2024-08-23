import string
import random
from MyPack2.Utilities import truncDecimal


def generate_id(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


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
        self.id = generate_id()
        self.target_list = []
        self.primary_target = None
        self.strength = 1
        self.camp_info = {}
        
    def __repr__(self):
        return self.nom if self.nom != "" else self.template

    def __copy__(self):
        """
        Programme permmettant de copier un object quelconque
          - Attention : newObject = Object_a_copier()
        """
        newObject = Division(self.template,0,0,0,0,0,0,0,0,0,0,0)
        for attr in self.__dict__:
            newObject.__setattr__(attr,self.__getattribute__(attr))
        newObject.id = generate_id()
        return newObject

    ############# COMBAT ####################

    def targeting(self, enemy_camp):
        engagement_width = self.width * 2
        enemy_divisions = enemy_camp.in_frontline
        target_list = []
        random.shuffle(enemy_divisions)

        # Creer la liste des divisions prise pour cible par :attacking_division:
        total_width = 0
        for enemy in enemy_divisions:
            if total_width + enemy.width <= engagement_width:
                target_list.append(enemy)
                total_width = sum(division.width for division in target_list)
            elif total_width == 0:
                target_list.append(enemy)
                break
            if all(div.width >= engagement_width for div in enemy_divisions):
                target_list.append(random.choice(enemy_divisions.divisions))
        self.target_list = target_list.copy()
        self.choose_priority_target()

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

    def do_attack(self):
        coordinated_share = 0.35 + self.camp_info["coordination"] * (1 + self.initiative)
        sa_per_division = (self.soft_attack * (1 - coordinated_share)) // len(self.target_list)
        ha_per_division = (self.hard_attack * (1 - coordinated_share)) // len(self.target_list)
        sa_for_primary  = self.soft_attack * coordinated_share
        ha_for_primary  = self.hard_attack * coordinated_share
        for target in self.target_list:
            if target == self.primary_target:
                total_sa = (sa_per_division + sa_for_primary) * (1 - target.hardness)
                total_ha = (ha_per_division + ha_for_primary) * target.hardness
            else:
                total_sa = sa_per_division * (1 - target.hardness)
                total_ha = ha_per_division * target.hardness
            total_attack = total_sa + total_ha
            total_attack = total_attack if self.piercing >= target.armor else total_attack/2
            total_attack /= 10
            target.take_damage(self,total_attack)

    def take_damage(self,striker,total_attack):
        # Hits calculation
        is_attacking = self.camp_info["is_attacking"]
        total_defense = self.attaque if is_attacking else self.defense
        if total_defense > total_attack:    total_attack *= 0.1
        else:                               total_attack  = total_defense*0.1 + (total_attack - total_defense)*0.4

        # HP Damage calculation
        #todo remplacer par des jets de dés
        self.pv -= 1.5*total_attack
        self.pv = truncDecimal(self.pv,1)
        self.pv = max(self.pv,0)

        # ORG Damage Calulation
        #todo remplacer par des jets de dés
        self.organisation -= 3.5 * total_attack if striker.piercing > self.hardness else 2.5 * total_attack
        self.organisation = truncDecimal(self.organisation, 1)
        self.organisation = max(self.organisation, 0)

        self.set_strength()

    def set_strength(self):
        self.strength = round(self.pv / self._PV,2)
        self.soft_attack = round(self._SOFT_ATTACK * self.strength)
        self.hard_attack = round(self._HARD_ATTACK * self.strength)
        self.defense = round(self._DEFENSE * self.strength)
        self.attaque = round(self._ATTAQUE * self.strength)

    ############# GESTION ####################

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

    @staticmethod
    def load(data):
        return Division(
            data["Nom de Template"], data["PV"], data["Organisation"], data["Soft Attack"], data["Hard Attack"],
            data["Defense"], data["Attaque"], data["Piercing"], data["Armor"], data["Hardness"], data["Width"],
            data["Initiative"]
        )