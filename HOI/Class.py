from MyPack.Utilities import *
from HOI.Tactics.Tactics_func import choose_tactic

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


#######################################################################################################################
#######################################################################################################################

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, attacker, defender):
        assert type(attacker) == Division and type(defender) == Division , "campA and campB must be division class"
        assert attacker.is_defending == False , "ATK.isDefending must be FALSE"
        assert defender.is_defending == True , "DEF.isDefending must be TRUE"
        self.attacker = attacker
        self.defender = defender
        self.attacker_tactic = None
        self.defender_tactic = None
        self.AttackerLeader = None
        self.DefenderLeader = None
        self.round_counter = 0
        self.Phase = "Default"
    def is_finnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        return any(val <= 0 for val in [self.attacker.pv,
                                        self.defender.pv,
                                        self.attacker.org,
                                        self.defender.org])  # Si PV ou orga des def ou attck est nulle ou moins

    def run_rounds(self, nb_rounds=1):
        """
        Definit le nombre de lancement de round
        :param nb_rounds: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        """
        assert type(nb_rounds) is int , "Nb must be an :int:"
        if nb_rounds != -1:
            i = 1
            while i <= nb_rounds: # Lancement de :Nb: rounds
                self._round()
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.is_finnish():
                self._round()
    def _round(self):
        """
        Lancement d'un round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        if self.round_counter % 12 == 0:  # Choix de Tactique tout les 12 rounds
            choose_tactic(self)
            txt = "New tactics / Battle phase: {}".format(self.Phase)
            txt += "\n- {} choose {} tactic".format(self.attacker.name, self.attacker_tactic)
            txt += "\n- {} choose {} tactic".format(self.defender.name, self.defender_tactic)
        self.attacker.do_attack(self.defender)  # ATK attaque
        self.defender.take_damage(self.attacker)   # DEF prend les dommages
        self.defender.do_attack(self.attacker)  # DEF riposte
        self.attacker.take_damage(self.defender)   # ATK prend les dommages
    # Log de fin de round
        self.round_counter += 1
        self.print_log()
    def print_log(self):
        """
        log pour chaque heure de combats
            - résulat des PV et ORG de chaques divisions
        """
        txt = """----------- round {} -----------------
DivATK: {}/{}   {}/{}
DivDEF: {}/{}   {}/{}""".format(self.round_counter,
                                self.attacker.pv, self.attacker._PVMAX, self.attacker.org, self.attacker._ORG,
                                self.defender.pv, self.defender._PVMAX, self.defender.org, self.defender._ORG)
        if self.is_finnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.round_counter)
        print(txt)