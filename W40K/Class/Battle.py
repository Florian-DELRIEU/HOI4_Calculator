from W40K.Functions.Functions import round_Stats
from W40K.Class.Regiment import Regiment
from W40K.Functions.Tactics_func import *
from W40K.Lists.Terrain_list import Terrain_dico
from W40K.Functions.Terrain_func import apply_Terrain
from MyPack.Utilities import AskUser
from W40K.Class.Leader import Leader

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, ATK, DEF, Terrain="Plains", River = None):
    # Initials conditions
        assert type(ATK) == Regiment and type(DEF) == Regiment , "campA and campB must be regiment class"
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
    # ATK team
        self.ATK = {
            "Regiment": ATK,
            "Tactic": Tactic,
            "Leader": Leader
        }
    # DEF Team
        self.DEF = {
            "Regiment":DEF,
            "Tactic":Tactic,
            "Leader":Leader
        }
    # Battle parameters
        self.roundCounter = 0
        self.CAC_level = 0
        self.CAC_limit = 0
        self.Current_Phase = "Default"  # Phase de bataille en cours
        self.Following_Phase = "Default"
        self.Terrain = Terrain_dico[Terrain]
        self.Terrain.set_River(River)
        self.Initiative_winner = None

    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        return (
                (self.ATK["Regiment"].HP  <= 0)
            or  (self.DEF["Regiment"].HP  <= 0)
            or  (self.ATK["Regiment"].ORG <= 0)
            or  (self.ATK["Regiment"].ORG <= 0)
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
                self._Round(Loglevel=LogLevel,PauseEachRound=False)

    def _init_round(self):
        apply_Terrain(self)
        update_CAC(self)

    def _Round(self,Loglevel,PauseEachRound=False):
        """
        Lancement d'une round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        txt = """----------- round {} -----------------""".format(self.roundCounter)
        self._init_round()
        if self.roundCounter%12 == 0:
            previous_CAC_limit = self.CAC_limit
            self.Current_Phase = self.Following_Phase
            choose_Tactics(self)
            if Loglevel:
                txt += "\nNew tactics / Battle phase: {}".format(self.Current_Phase)
                txt += "\n- {} choose {} tactic".format(self.ATK["Regiment"].Name,self.ATK["Tactic"])
                txt += "\n- {} choose {} tactic".format(self.DEF["Regiment"].Name,self.DEF["Tactic"])
                txt += "\n"
                txt += "\nOld CAC limit = {}".format(previous_CAC_limit)
        if self.roundCounter%12 == 0 and Loglevel:
            txt += "\n- Cac changes by ATK = {}".format(self.ATK["Tactic"].CAC)
            txt += "\n- Cac changes by DEF = {}".format(self.DEF["Tactic"].CAC)
            txt += "\nNew CAC limit = {}".format(self.CAC_limit)
        txt += "\nNew cac_level = {}".format(self.CAC_level)
        txt += "\n"
    # Stats arrondis
        round_Stats(self.ATK)
        round_Stats(self.DEF)
        round_Stats(self)
    # ATK Round
        self.ATK["Regiment"].Attaque(self.DEF,self.CAC_level)  # ATK attaque
        if Loglevel:
            txt += "\n{} round".format(self.ATK["Regiment"].Name)
            txt += "\n - Shots: {} SA + {} HA = {}".format(self.ATK["Regiment"].SoftAttack,self.ATK["Regiment"].HardAttack,
                                                           self.ATK["Regiment"].SoftAttack+self.ATK["Regiment"].HardAttack)
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.ATK["Regiment"].SoftMeleeAttack*self.CAC_level,2),
                                                             round(self.ATK["Regiment"].HardMeleeAttack*self.CAC_level,2),
                    round(self.ATK["Regiment"].SoftMeleeAttack*self.CAC_level,2)+round(self.ATK["Regiment"].SoftMeleeAttack*self.CAC_level,2))
    # DEF Round
        self.DEF["Regiment"].Attaque(self.DEF,self.CAC_level)  # DEF riposte
        if Loglevel:
            txt += "\n{} round".format(self.DEF["Regiment"].Name)
            txt += "\n - Shots: {} SA + {} HA = {}".format(self.DEF["Regiment"].SoftAttack, self.DEF["Regiment"].HardAttack,
                                                           self.DEF["Regiment"].SoftAttack + self.DEF["Regiment"].HardAttack)
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.DEF["Regiment"].SoftMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF["Regiment"].HardMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF["Regiment"].SoftMeleeAttack*self.CAC_level, 2) + round(
                                                                 self.DEF["Regiment"].SoftMeleeAttack*self.CAC_level, 2))
        self.DEF["Regiment"].Damage(self.ATK)   # DEF prend les dommages
        if Loglevel: txt+= "\n{} takes {} hits (-{} defenses)".format(self.DEF["Regiment"].Name,self.ATK["Regiment"].NbATK,self.DEF["Regiment"].Defense)
        self.ATK["Regiment"].Damage(self.DEF)   # ATK prend les dommages
        if Loglevel: txt+= "\n{} takes {} hits (-{} breakthrought)".format(self.ATK["Regiment"].Name,self.DEF["Regiment"].NbATK,self.ATK["Regiment"].Breakthrought)
        print(txt)
    # Log de fin de round
        self.roundCounter += 1
        self.printLOG()
        if PauseEachRound: AskUser("pausing ...","Click Enter")

    def set_River(self,River_width):
        self.Terrain.set_River(River_width=River_width)

    def printLOG(self):
        """
        log pour chaque heure de combats
        """
        txt= """{}: {}/{}   {}/{}
{}: {}/{}   {}/{}

""".format(self.ATK["Regiment"].Name,self.ATK["Regiment"].HP,self.ATK["Regiment"]._Regiment__HP,self.ATK["Regiment"].ORG,self.ATK["Regiment"]._Regiment__ORG,
           self.DEF["Regiment"].Name,self.DEF["Regiment"].HP,self.DEF["Regiment"]._Regiment__HP,self.DEF["Regiment"].ORG,self.DEF["Regiment"]._Regiment__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)
