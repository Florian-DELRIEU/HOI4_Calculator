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
        assert ATK.is_defending == False , "ATK.isDefending must be FALSE"
        assert DEF.is_defending == True , "DEF.isDefending must be TRUE"
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
            or  (self.ATK.org <= 0)
            or  (self.DEF.org <= 0)
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
        txt = f"""----------- round {self.roundCounter} -----------------"""
        if self.roundCounter%12 == 0:
            previous_CAC_limit = self.CAC_limit
            choose_Tactics(self)
            if Loglevel:
                txt += f"\nNew tactics / Battle phase: {self.Phase}"
                txt += f"\n- {self.ATK.name} choose {self.ATK_Tactic} tactic"
                txt += f"\n- {self.DEF.name} choose {self.DEF_Tactic} tactic"
                txt += "\n"
                txt += f"\nOld CAC limit = {previous_CAC_limit}"
        update_CAC(self)
        if self.roundCounter%12 == 0 and Loglevel:
            txt += f"\n- Cac changes by ATK = {self.ATK_Tactic.CAC}"
            txt += f"\n- Cac changes by DEF = {self.DEF_Tactic.CAC}"
            txt += f"\nNew CAC limit = {self.CAC_limit}"
        txt += f"\nNew cac_level = {self.CAC_level}"
        txt += "\n"
    # Stats arrondis
        round_Stats(self.ATK)
        round_Stats(self.DEF)
        round_Stats(self)
    # ATK Round
        self.ATK.do_attack(self.DEF, self.CAC_level)  # ATK attaque
        if Loglevel:
            txt += f"\n{self.ATK.name} round"
            txt += f"\n - Shots: {self.ATK.SoftAttack} SA + {self.ATK.HardAttack} HA = {self.ATK.SoftAttack + self.ATK.HardAttack}"
            txt += f"\n - Melee: {round(self.ATK.SoftMeleeAttack * self.CAC_level, 2)} SMA + {round(self.ATK.HardMeleeAttack * self.CAC_level, 2)} HMA = {round(self.ATK.SoftMeleeAttack * self.CAC_level, 2) + round(self.ATK.SoftMeleeAttack * self.CAC_level, 2)}"
    # DEF Round
        self.DEF.do_attack(self.DEF, self.CAC_level)  # DEF riposte
        if Loglevel:
            txt += f"\n{self.DEF.name} round"
            txt += f"\n - Shots: {self.DEF.SoftAttack} SA + {self.DEF.HardAttack} HA = {self.DEF.SoftAttack + self.DEF.HardAttack}"
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.DEF.SoftMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF.HardMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF.SoftMeleeAttack*self.CAC_level, 2) + round(
                                                                 self.DEF.SoftMeleeAttack*self.CAC_level, 2))
        self.DEF.take_damage(self.ATK)   # DEF prend les dommages
        if Loglevel:
            txt += f"\n{self.DEF.name} takes {self.ATK.nbr_attack} hits (-{self.DEF.Defense} defenses)"
        self.ATK.take_damage(self.DEF)   # ATK prend les dommages
        if Loglevel:
            txt += f"\n{self.ATK.name} takes {self.DEF.nbr_attack} hits (-{self.ATK.Breakthrought} breakthrought)"
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

""".format(self.ATK.name, self.ATK.HP, self.ATK._Regiment__HP, self.ATK.org, self.ATK._Regiment__ORG,
           self.DEF.name, self.DEF.HP, self.DEF._Regiment__HP, self.DEF.org, self.DEF._Regiment__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)
