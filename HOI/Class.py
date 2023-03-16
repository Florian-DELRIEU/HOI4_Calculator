from MyPack.Utilities import *
from HOI.Tactics.Tactics_func import choose_Tactic

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
        self.NAME = name
        self.set_str()  # Mets a jour les stat en fonction des PV de la division
        self.is_defending = True # TRUE si la division et en défense

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
    def Attaque(self,Target):
        """
        Calcul du nombre d'attaque de :self: sur :Target:
        :param Target: division cible de :self:
        """
        self.set_str() # MAJ des stats
        nb_atk = Target.hard*self.ha + (1 - Target.hard)*self.sa  # Calcul du nbr d'attaque en fonction du Hardness
    # Piercing ?
        self.nb_atk = nb_atk if self.prc >= Target.arm else nb_atk/2
        self.nb_atk /= 10 # les attaques sont divisé par 10 (voir wiki)
    def Damage(self,Striker):
        """
        Calcul du nombre de touche et des dégats
        :param Striker: Division attaquante
        """
        self.set_str() # MAJ
        nb_damage = Striker.nb_atk #Recupere le nombre d'attaque de l'attaquant
    # Attaquant ou defenseur ?
        current_defense = self.defense if self.is_defending else self.attack
    # Defense de la cible
        if current_defense > nb_damage: nb_damage *= 0.1
        else:                           nb_damage = self.defense*0.1 + (nb_damage - self.defense)*0.4
    # Calcul des dégats entre les PV et l'ORG
    # PV Dégats
        self.pv -= 1.5*nb_damage # Moyenne de D2
        self.pv = truncDecimal(self.pv, 1)
        self.pv = max(self.pv, 0)
    # ORG Dégats
        self.org -= 3.5*nb_damage if self.prc > Striker.arm else 2.5*nb_damage
        self.org = truncDecimal(self.org, 1)
        self.org = max(self.org, 0)

class Bataillon:
    def __init__(self,PV,ORG,SA,HA,DEF,BRK,ARM,PRC,HARD,Width,Supply_use,Fuel_use,IC,Name=""):
        self.PV = PV
        self.ORG = ORG
        self.SA = SA
        self.HA = HA
        self.DEF = DEF
        self.BRK = BRK
        self.ARM = ARM
        self.PRC = PRC
        self.HARD = HARD
        self.Width = Width
        self.Supply_use = Supply_use
        self.Fuel_use = Fuel_use
        self.IC = IC
        self.Name = Name


#######################################################################################################################
#######################################################################################################################

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, ATK, DEF):
        assert type(ATK) == Division and type(DEF) == Division , "campA and campB must be division class"
        assert ATK.is_defending == False , "ATK.isDefending must be FALSE"
        assert DEF.is_defending == True , "DEF.isDefending must be TRUE"
        self.ATK = ATK
        self.DEF = DEF
        self.ATK_Tactic = None
        self.DEF_Tactic = None
        self.ATK_Leader = None
        self.DEF_Leader = None
        self.roundCounter = 0
        self.Phase = "Default"
    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        return (
            (self.ATK.pv <= 0)
            or (self.DEF.pv <= 0)
            or (self.ATK.org <= 0)
            or (self.DEF.org <= 0)
        )
    def Round(self,Nb=1):
        """
        Definit le nombre de lancement de round
        :param Nb: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        """
        assert type(Nb) is int , "Nb must be an :int:"
        if Nb != -1:
            i = 1
            while i <= Nb: # Lancement de :Nb: rounds
                self._Round()
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.isFinnish():
                self._Round()
    def _Round(self):
        """
        Lancement d'un round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        if self.roundCounter % 12 == 0:  # Choix de Tactique tout les 12 rounds
            choose_Tactic(self)
            txt = "New tactics / Battle phase: {}".format(self.Phase)
            txt += "\n- {} choose {} tactic".format(self.ATK.name, self.ATK_Tactic)
            txt += "\n- {} choose {} tactic".format(self.DEF.name, self.DEF_Tactic)
        self.ATK.Attaque(self.DEF)  # ATK attaque
        self.DEF.Damage(self.ATK)   # DEF prend les dommages
        self.DEF.Attaque(self.ATK)  # DEF riposte
        self.ATK.Damage(self.DEF)   # ATK prend les dommages
    # Log de fin de round
        self.roundCounter += 1
        self.printLOG()
    def printLOG(self):
        """
        log pour chaque heure de combats
            - résulat des PV et ORG de chaques divisions
        """
        txt = """----------- round {} -----------------
DivATK: {}/{}   {}/{}
DivDEF: {}/{}   {}/{}""".format(self.roundCounter,
                                self.ATK.pv, self.ATK._PVMAX, self.ATK.org, self.ATK._ORG,
                                self.DEF.pv, self.DEF._PVMAX, self.DEF.org, self.DEF._ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)