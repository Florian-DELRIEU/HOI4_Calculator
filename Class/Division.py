from MyPack2.Utilities import truncDecimal

class Division:
    """
    Objet division
    self._Stat : stats de la division quand elle est en pleine santé "strenght = 1"
    self.Stat  : Stats de la division
    """
    def __init__(self, pv_max, org, sa, ha, defense, attack, piercing, armor, hard, entrenchment, name=""):
        self._PVMAX = pv_max
        self._ORG = org
        self._SA = sa # Soft Attack
        self._HA = ha # Hard Attack
        self._DEFENSE = defense # Defense
        self._ATTACK = attack # Breakthought
        self.pv = self._PVMAX
        self.org = self._ORG
        self.prc = piercing # Piercing
        self.arm = armor # Armor
        self.hard = hard # Hardness
        self.rtch = entrenchment # Retranchement
        self.defense = self._DEFENSE
        self.attack = self._ATTACK
        self.nb_atk = 0
        self.name = name
        self.set_str()  # Mets a jour les stat en fonction des PV de la division
        self.is_defending = True # TRUE si la division et en défense

    def __repr__(self):
        return self.name

    def set_str(self):
        """
        Calcul de la STR en fonction des PV
        """
        self.str = self.pv/self._PVMAX
    # MAJ des stats en fonction de STR
        self.sa = self._SA*self.str
        self.ha = self._HA*self.str
        self.defense = self._DEFENSE*self.str
        self.attack = self._ATTACK*self.str
    def do_attack(self, target):
        """
        Calcul du nombre d'attaque de :self: sur :Target:
        :param target: division cible de :self:
        """
        self.set_str() # MAJ des stats
        nb_atk = target.hard*self.ha + (1 - target.hard)*self.sa  # Calcul du nbr d'attaque en fonction du Hardness
    # Piercing ?
        self.nb_atk = nb_atk if self.prc >= target.arm else nb_atk/2
        self.nb_atk /= 10 # les attaques sont divisé par 10 (voir wiki)
    def take_damage(self, striker):
        """
        Calcul du nombre de touche et des dégats
        :param striker: Division attaquante
        """
        self.set_str() # MAJ
        nb_damage = striker.nb_atk #Recupere le nombre d'attaque de l'attaquant
    # Attaquant ou defenseur ?
        tmp_defense = self.defense if self.is_defending else self.attack
    # Defense de la cible
        if tmp_defense > nb_damage:     nb_damage *= 0.1
        else:                           nb_damage = self.defense*0.1 + (nb_damage - self.defense)*0.4
    # Calcul des dégats entre les PV et l'ORG
    # PV Dégats
        self.pv -= 1.5*nb_damage # Moyenne de D2
        self.pv = truncDecimal(self.pv, 1)
        self.pv = max(self.pv, 0)
    # ORG Dégats
        self.org -= 3.5*nb_damage if self.prc > striker.arm else 2.5*nb_damage
        self.org = truncDecimal(self.org, 1)
        self.org = max(self.org, 0)