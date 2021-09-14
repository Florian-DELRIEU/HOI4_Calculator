from W40K.FuncAndTables.Functions import round_Stats
from W40K.LandBattles.Company import Regiment
from W40K.LandBattles.Tactics.Tactics_func import *

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, ATK, DEF):
        assert type(ATK) == Regiment and type(DEF) == Regiment , "campA and campB must be regiment class"
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
        self.ATK_Tactic = None
        self.DEF_Tactic = None
        self.ATK = ATK
        self.DEF = DEF
        self.roundCounter = 0
        self.CAC_level = 0
        self.CAC_limit = 0
    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        if (self.ATK.HP <= 0) or (self.DEF.HP <= 0) or (self.ATK.ORG <= 0) or (self.DEF.ORG <= 0):
            return True
        else:
            return False
    def Round(self,Nb=1,LogLevel=True):
        """
        Definit le nombre de lancement de round
        :param Nb: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        """
        assert type(Nb) is int , "Nb must be an :int:"
        if Nb != -1:
            i = 1
            while i <= Nb: # Lancement de :Nb: rounds
                self._Round(Loglevel=LogLevel)
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.isFinnish():
                self._Round(Loglevel=LogLevel)
    def _Round(self,Loglevel):
        """
        Lancement d'une round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        if self.roundCounter%12 == 0:
            choose_Tactics(self)
        update_CAC(self)
    # Stats arrondis
        round_Stats(self.ATK)
        round_Stats(self.DEF)
        round_Stats(self)
        print("""----------- round {} -----------------""".format(self.roundCounter))
    # Round
        self.ATK.Attaque(self.DEF,self.CAC_level)  # ATK attaque
        txt = "ATK shot {} SA + {} HA // {} SMA + {} HMA".format(self.ATK.SoftAttack,self.ATK.HardAttack,
                                                                 round(self.ATK.SoftMeleeAttack*self.CAC_level,2),
                                                                 round(self.ATK.HardMeleeAttack*self.CAC_level,2))
        self.DEF.Attaque(self.ATK,self.CAC_level)  # DEF riposte
        txt+= "\nDEF shot {} SA + {} HA // {} SMA + {} HMA".format(self.DEF.SoftAttack, self.DEF.HardAttack,
                                                                 round(self.DEF.SoftMeleeAttack*self.CAC_level,2),
                                                                 round(self.DEF.HardMeleeAttack*self.CAC_level,2))
        self.DEF.Damage(self.ATK)   # DEF prend les dommages
        txt+= "\nATK: {} --->> // {} DEF".format(self.ATK.NbATK,self.DEF.Defense)
        self.ATK.Damage(self.DEF)   # ATK prend les dommages
        txt+= "\nDEF: {} --->> // {} ATK".format(self.DEF.NbATK,self.ATK.Breakthrought)
        if Loglevel: print(txt)
    # Log de fin de round
        self.roundCounter += 1
        self.printLOG()
    def printLOG(self):
        """
        log pour chaque heure de combats
        """
        txt= """{}: {}/{}   {}/{}
{}: {}/{}   {}/{}

""".format(self.ATK.Name,self.ATK.HP,self.ATK._Regiment__HP,self.ATK.ORG,self.ATK._Regiment__ORG,
           self.DEF.Name,self.DEF.HP,self.DEF._Regiment__HP,self.DEF.ORG,self.DEF._Regiment__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)