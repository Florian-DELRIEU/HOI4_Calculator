from MyPack.Utilities import *

class Division:
    """
    Objet division
    self._Stat : stats de la division quand elle est en pleine santé "strenght = 1"
    self.Stat  : Stats de la division
    """
    def __init__(self,PV,ORG,SA,HA,DEF,BRK,PRC,ARM,HARD,RTCH,Name=""):
        self._PVmax = PV
        self._ORG = ORG
        self._SA = SA # Soft Attack
        self._HA = HA # Hard Attack
        self._DEF = DEF # Defense
        self._BRK = BRK # Breakthought
        self.PV = self._PVmax
        self.ORG = self._ORG
        self.PRC = PRC # Piercing
        self.ARM = ARM # Armor
        self.HARD = HARD # Hardness
        self.RTCH = RTCH # Retranchement
        self.NbATK = 0
        self.Name = ""
        self.set_STR()  # Mets a jour les stat en fonction des PV de la division
        self.isDefending = True # TRUE si la division et en défense
    def set_STR(self):
        """
        Calcul de la STR en fonction des PV
        """
        self.STR = self.PV / self._PVmax
    # MAJ des stats en fonction de STR
        self.SA = self._SA * self.STR
        self.HA = self._HA * self.STR
        self.DEF = self._DEF * self.STR
        self.BRK = self._BRK * self.STR
    def Attaque(self,Target):
        """
        Calcul du nombre d'attaque de :self: sur :Target:
        :param Target: division cible de :self:
        """
        self.set_STR() # MAJ des stats
        NbATK = Target.HARD*self.HA + (1-Target.HARD)*self.SA  # Calcul du nbr d'attaque en fonction du Hardness
    # Piercing ?
        if self.PRC <= Target.ARM: self.NbATK = NbATK/2  # si perce pas
        else: self.NbATK = NbATK                     # si perce
        self.NbATK /= 10 # les attaques sont divisé par 10 (voir wiki)
    def Damage(self,Striker):
        """
        Calcul du nombre de touche et des dégats
        :param Striker: Division attaquante
        """
        self.set_STR() # MAJ
        NbDAMAGE = Striker.NbATK #Recupere le nombre d'attaque de l'attaquant
    # Attaquant ou defenseur ?
        if self.isDefending: DEF = self.DEF  # Si defend alors utilise DEFENSE stat
        else:                DEF = self.BRK  # si attaque alors utilise BREAKTOUGHT stat
    # Defense de la cible
        if DEF > NbDAMAGE: NbDAMAGE *= 0.1
        else:              NbDAMAGE = self.DEF*0.1 + (NbDAMAGE-self.DEF)*0.4
    # Calcul des dégats entre les PV et l'ORG
    # PV Dégats
        self.PV -= 1.5*NbDAMAGE # Moyenne de D2
        self.PV = truncDecimal(self.PV,1)
        if self.PV <= 0 : self.PV = 0
    # ORG Dégats
        if self.PRC > Striker.ARM:
            self.ORG -= 3.5*NbDAMAGE # Moyenne de D6
        else:
            self.ORG -= 2.5*NbDAMAGE # Moyenne de D4
        self.ORG = truncDecimal(self.ORG,1)
        if self.ORG <= 0 : self.ORG = 0

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
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
        self.ATK = ATK
        self.DEF = DEF
        self.roundCounter = 0
    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        if (self.ATK.PV <= 0) or (self.DEF.PV <= 0) or (self.ATK.ORG <= 0) or (self.DEF.ORG <= 0):
            return True
        else:
            return False
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
                                self.ATK.PV,self.ATK._PVmax,self.ATK.ORG,self.ATK._ORG,
                                self.DEF.PV,self.DEF._PVmax,self.DEF.ORG,self.DEF._ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)