from W40K.Class.Regiment import Regiment
from W40K.Class.Leader import Leader

from W40K.Functions.Tactics_func import *
from W40K.Functions.Functions import round_Stats
from W40K.Functions.Terrain_func import apply_Terrain
from W40K.Functions.Leader_func import set_LeaderSkills, apply_LeaderTactic

from W40K.Lists.Terrain_list import Terrain_dico
from W40K.Lists.Tactics_list import ATK_all_tactics,DEF_all_tactics
from MyPack.Utilities import AskUser

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self,
                 ATK, DEF, ATK_leader=Leader(1,1,1,[],[]), DEF_leader=Leader(1,1,1,[],[]),
                 Terrain="Plains", River = None
                 ):
    # Initials conditions
        assert type(ATK) == Regiment and type(DEF) == Regiment , "campA and campB must be regiment class"
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
        self.ATK = {
            "Regiment": ATK,
            "Leader": ATK_leader,
            "Tactics": ATK_all_tactics.copy()
        }
        self.ATK_Tactic_chosen = None
        self.DEF = {
            "Regiment":DEF,
            "Leader":DEF_leader,
            "Tactics":DEF_all_tactics.copy()
        }
        self.DEF_Tactic_chosen = None
    # Battle parameters
        self.roundCounter = 0
        self.CAC_level = 0
        self.CAC_limit = 0
        self.Current_Phase = "Default"  # Phase de bataille en cours
        self.Following_Phase = "Default"
        self.Terrain = Terrain_dico[Terrain]
        self.River = River
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
            or  (self.DEF["Regiment"].ORG <= 0)
        )

    def _init_round(self):
        self.Terrain.set_River(self.River)
        set_LeaderSkills(self)
        apply_LeaderTactic(self)
        apply_Terrain(self)
        update_CAC(self)
        self.apply_river()

    def apply_river(self):
        """
        TODO - Move function to Terrain_func
        :return:
        """
        if self.River is None:
            for side in [self.ATK,self.DEF]:
                for tactic in side["Tactics"]:
                    if "Bridge" in tactic.Name:
                        tactic.weight = 0

    def Round(self,Nb:int()=1,LogLevel=True):
        """
        -   Definit le nombre de lancement de round
        -   run _Round
        :param Nb: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        :param LogLevel:
        """
        if Nb != -1:
            i = 1
            while i <= Nb and not self.isFinnish(): # Lancement de :Nb: rounds
                self._Round(Loglevel=LogLevel)
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.isFinnish():
                self._Round(Loglevel=LogLevel,PauseEachRound=False)

    def _Round(self,Loglevel,PauseEachRound=False):
        ATK_regiment = self.ATK["Regiment"]
        DEF_regiment = self.DEF["Regiment"]
        """
        Lancement d'une round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        txt = f"""----------- round {self.roundCounter} -----------------"""
        self._init_round()
        if self.roundCounter%12 == 0:
            previous_CAC_limit = self.CAC_limit
            self.Current_Phase = self.Following_Phase
            choose_Tactics(self)
            if Loglevel:
                txt += f"\nNew tactics / Battle phase: {self.Current_Phase}"
                txt += f"\n- {ATK_regiment.Name} choose {self.ATK_Tactic_chosen} tactic"
                txt += f"\n- {DEF_regiment.Name} choose {self.DEF_Tactic_chosen} tactic"
                txt += "\n"
                txt += f"\nOld CAC limit = {previous_CAC_limit}"
        if self.roundCounter%12 == 0 and Loglevel:
            txt += f"\n- Cac changes by ATK = {self.ATK_Tactic_chosen.CAC}"
            txt += f"\n- Cac changes by DEF = {self.DEF_Tactic_chosen.CAC}"
            txt += f"\nNew CAC limit = {self.CAC_limit}"
        txt += f"\nNew cac_level = {self.CAC_level}"
        txt += "\n"
    # Stats arrondis
        round_Stats(ATK_regiment)
        round_Stats(DEF_regiment)
        round_Stats(self)
    # ATK Round
        ATK_regiment.Attaque(DEF_regiment,self.CAC_level)  # ATK attaque
        if Loglevel:
            txt += f"\n{ATK_regiment.Name} round"
            txt += f"\n - Shots: {ATK_regiment.SoftAttack} SA + {ATK_regiment.HardAttack} HA = {ATK_regiment.SoftAttack + ATK_regiment.HardAttack}"
            txt += f"\n - Melee: {round(ATK_regiment.SoftMeleeAttack * self.CAC_level, 2)} SMA + {round(ATK_regiment.HardMeleeAttack * self.CAC_level, 2)} HMA = {round(ATK_regiment.SoftMeleeAttack * self.CAC_level, 2) + round(ATK_regiment.SoftMeleeAttack * self.CAC_level, 2)}"
    # DEF Round
        DEF_regiment.Attaque(DEF_regiment,self.CAC_level)  # DEF riposte
        if Loglevel:
            txt += f"\n{DEF_regiment.Name} round"
            txt += f"\n - Shots: {DEF_regiment.SoftAttack} SA + {DEF_regiment.HardAttack} HA = {DEF_regiment.SoftAttack + DEF_regiment.HardAttack}"
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(DEF_regiment.SoftMeleeAttack*self.CAC_level, 2),
                                                             round(DEF_regiment.HardMeleeAttack*self.CAC_level, 2),
                                                             round(DEF_regiment.SoftMeleeAttack*self.CAC_level, 2) + round(
                                                                 DEF_regiment.SoftMeleeAttack*self.CAC_level, 2))
        DEF_regiment.Damage(ATK_regiment)   # DEF prend les dommages
        if Loglevel:
            txt += f"\n{DEF_regiment.Name} takes {ATK_regiment.NbATK} hits (-{DEF_regiment.Defense} defenses)"
        ATK_regiment.Damage(DEF_regiment)   # ATK prend les dommages
        if Loglevel:
            txt += f"\n{ATK_regiment.Name} takes {DEF_regiment.NbATK} hits (-{ATK_regiment.Breakthrought} breakthrought)"
        print(txt)
    # Log de fin de round
        self.roundCounter += 1
        self.printLOG()
        if PauseEachRound: AskUser("pausing ...","Click Enter")

    def printLOG(self):
        """
        log pour chaque heure de combats
        """
        ATK_regiment = self.ATK["Regiment"]
        DEF_regiment = self.DEF["Regiment"]
        txt= """{}: {}/{}   {}/{}
{}: {}/{}   {}/{}

""".format(ATK_regiment.Name,ATK_regiment.HP,ATK_regiment._Regiment__HP,ATK_regiment.ORG,ATK_regiment._Regiment__ORG,
           DEF_regiment.Name,DEF_regiment.HP,DEF_regiment._Regiment__HP,DEF_regiment.ORG,DEF_regiment._Regiment__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)
