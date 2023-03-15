from W40K.Functions.Functions import round_Stats
from W40K.Class.Regiment import Regiment
from W40K.Functions.Tactics_func import *
from MyPack.Utilities import AskUser

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, ATK, DEF):
    # Initials conditions
        assert type(ATK) == Regiment and type(DEF) == Regiment , "campA and campB must be regiment class"
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
    # ATK team
        self.ATK = ATK
        self.ATK_Tactic = None
        self.ATK_Leader = None
    # DEF Team
        self.DEF = DEF
        self.DEF_Tactic = None
        self.DEF_Leader = None
    # Battle parameters
        self.roundCounter = 0
        self.CAC_level = 0
        self.CAC_limit = 0
        self.Phase = "Default"  # Phase de bataille en cours
        self.Terrain = "Plain"
    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        return (
                (self.ATK.HP  <= 0)
            or  (self.DEF.HP  <= 0)
            or  (self.ATK.ORG <= 0)
            or  (self.DEF.ORG <= 0)
        )
    def Round(self,Nb:int()=1,LogLevel=True):
        """
        -   Definit le nombre de lancement de round
        -   run _Round
        :param Nb: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        """
        if Nb != -1:
            i = 1
            while i <= Nb and not self.isFinnish(): # Lancement de :Nb: rounds
                self._Round(Loglevel=LogLevel)
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.isFinnish():
                self._Round(Loglevel=LogLevel,PauseEachRound=True)
    def _Round(self,Loglevel,PauseEachRound=False):
        """
        Lancement d'une round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        txt = """----------- round {} -----------------""".format(self.roundCounter)
        if self.roundCounter%12 == 0:
            previous_CAC_limit = self.CAC_limit
            choose_Tactics(self)
            if Loglevel:
                txt += "\nNew tactics / Battle phase: {}".format(self.Phase)
                txt += "\n- {} choose {} tactic".format(self.ATK.name, self.ATK_Tactic)
                txt += "\n- {} choose {} tactic".format(self.DEF.name, self.DEF_Tactic)
                txt += "\n"
                txt += "\nOld CAC limit = {}".format(previous_CAC_limit)
        update_CAC(self)
        if self.roundCounter%12 == 0 and Loglevel:
            txt += "\n- Cac changes by ATK = {}".format(self.ATK_Tactic.CAC)
            txt += "\n- Cac changes by DEF = {}".format(self.DEF_Tactic.CAC)
            txt += "\nNew CAC limit = {}".format(self.CAC_limit)
        txt += "\nNew cac_level = {}".format(self.CAC_level)
        txt += "\n"
    # Stats arrondis
        round_Stats(self.ATK)
        round_Stats(self.DEF)
        round_Stats(self)
    # ATK Round
        self.ATK.Attaque(self.DEF,self.CAC_level)  # ATK attaque
        if Loglevel:
            txt += "\n{} round".format(self.ATK.name)
            txt += "\n - Shots: {} SA + {} HA = {}".format(self.ATK.SoftAttack,self.ATK.HardAttack,
                                                         self.ATK.SoftAttack+self.ATK.HardAttack)
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.ATK.SoftMeleeAttack*self.CAC_level,2),
                                                             round(self.ATK.HardMeleeAttack*self.CAC_level,2),
                    round(self.ATK.SoftMeleeAttack*self.CAC_level,2)+round(self.ATK.SoftMeleeAttack*self.CAC_level,2))
    # DEF Round
        self.DEF.Attaque(self.DEF,self.CAC_level)  # DEF riposte
        if Loglevel:
            txt += "\n{} round".format(self.DEF.name)
            txt += "\n - Shots: {} SA + {} HA = {}".format(self.DEF.SoftAttack, self.DEF.HardAttack,
                                                           self.DEF.SoftAttack + self.DEF.HardAttack)
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.DEF.SoftMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF.HardMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF.SoftMeleeAttack*self.CAC_level, 2) + round(
                                                                 self.DEF.SoftMeleeAttack*self.CAC_level, 2))
        self.DEF.Damage(self.ATK)   # DEF prend les dommages
        if Loglevel: txt+= "\n{} takes {} hits (-{} defenses)".format(self.DEF.name, self.ATK.nbr_attack, self.DEF.Defense)
        self.ATK.Damage(self.DEF)   # ATK prend les dommages
        if Loglevel: txt+= "\n{} takes {} hits (-{} breakthrought)".format(self.ATK.name, self.DEF.nbr_attack, self.ATK.Breakthrought)
        print(txt)
    # Log de fin de round
        self.roundCounter += 1
        self.printLOG()
        if PauseEachRound: AskUser("pausing ...","Click Enter")
    def printLOG(self):
        """
        log pour chaque heure de combats
        """
        txt= """{}: {}/{}   {}/{}
{}: {}/{}   {}/{}

""".format(self.ATK.name, self.ATK.HP, self.ATK._Regiment__HP, self.ATK.ORG, self.ATK._Regiment__ORG,
           self.DEF.name, self.DEF.HP, self.DEF._Regiment__HP, self.DEF.ORG, self.DEF._Regiment__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)
