from W40K.Functions.Functions import round_Stats
from W40K.Class.Regiment import Regiment
from W40K.Functions.Tactics_func import *
from MyPack.Utilities import AskUser
from numpy.random import choice
from numpy import sum

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, ATK_list, DEF_list):
    # Initials conditions
        assert [type(ATK) == Regiment for ATK in ATK_list] , "List have to contain regiments"
        assert [type(DEF) == Regiment for DEF in DEF_list] , "List have to contain regiments"
        for ATK in ATK_list: ATK.isDefending == False
        for DEF in DEF_list: DEF.isDefending == True
    # ATK team
        self.ATK_list = ATK_list
        self.ATK_Tactic = None
        self.ATK_Leader = None
        self.ATK_Engaged = []
        self.ATK_Reserve = []
    # DEF Team
        self.DEF_list = DEF_list
        self.DEF_Tactic = None
        self.DEF_Leader = None
        self.DEF_Engaged = []
        self.DEF_Reserve = []
    # Battle parameters
        self.Width = 80
        self.roundCounter = 0
        self.CAC_level = 0
        self.CAC_limit = 0
        self.Phase = "Default"  # Phase de bataille en cours
        self.Terrain = "Plain"
    def set_Engagement(self):
        """
        Defini l'engagement des Régiment en fonctions du Width
        """
        self._set_Engagment(self.ATK_list)
        self._set_Engagment(self.DEF_list)
    def _set_Engagment(self,List):
        """
        TODO -- Regle engagements (Voir règles d'engagement sur le wiki)
            1) Toutes les regiments qui ne sont pas engagé vont dans les réserves
            2) Si il reste de la place dans la liste des regiments engagés
                2A)- si aucun regiment est engagés en choisir selon Initiative
                2B)- si il reste de la place
                    a)- chaque regiment à 2% de chances de s'engager
                    b)- Proba modifié par radio (initiative), vitesse, technologie et doctrines
            3) Si une unité en 1ere ligne n'as plus d'ORG/PV alors elle fuit
            4) si toutes les unités en premières ligne fuit alors la bataille est perdu
        """
        Regiment_list = List
        current_width = np.sum([reg.Width for reg in Regiment_list])
    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        return (
                (len(self.ATK_Engaged) == 0)
            or  (len(self.DEF_Engaged) == 0)
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
                txt += f"\nNew tactics / Battle phase: {self.Phase}"
                txt += f"\n- ATK choose {self.ATK_Tactic} tactic"
                txt += f"\n- DEF choose {self.DEF_Tactic} tactic"
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
        round_Stats(iter(self.ATK_list))
        round_Stats(iter(self.DEF_list))
        round_Stats(self)
    # ATK Round
        self.ATK.Attaque(self.DEF,self.CAC_level)  # ATK attaque
        if Loglevel:
            txt += "\n{} round".format(self.ATK.Name)
            txt += "\n - Shots: {} SA + {} HA = {}".format(self.ATK.SoftAttack,self.ATK.HardAttack,
                                                         self.ATK.SoftAttack+self.ATK.HardAttack)
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.ATK.SoftMeleeAttack*self.CAC_level,2),
                                                             round(self.ATK.HardMeleeAttack*self.CAC_level,2),
                    round(self.ATK.SoftMeleeAttack*self.CAC_level,2)+round(self.ATK.SoftMeleeAttack*self.CAC_level,2))
    # DEF Round
        self.DEF.Attaque(self.DEF,self.CAC_level)  # DEF riposte
        if Loglevel:
            txt += "\n{} round".format(self.DEF.Name)
            txt += "\n - Shots: {} SA + {} HA = {}".format(self.DEF.SoftAttack, self.DEF.HardAttack,
                                                           self.DEF.SoftAttack + self.DEF.HardAttack)
            txt += "\n - Melee: {} SMA + {} HMA = {}".format(round(self.DEF.SoftMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF.HardMeleeAttack*self.CAC_level, 2),
                                                             round(self.DEF.SoftMeleeAttack*self.CAC_level, 2) + round(
                                                                 self.DEF.SoftMeleeAttack*self.CAC_level, 2))
        self.DEF.Damage(self.ATK)   # DEF prend les dommages
        if Loglevel: txt+= "\n{} takes {} hits (-{} defenses)".format(self.DEF.Name,self.ATK.NbATK,self.DEF.Defense)
        self.ATK.Damage(self.DEF)   # ATK prend les dommages
        if Loglevel: txt+= "\n{} takes {} hits (-{} breakthrought)".format(self.ATK.Name,self.DEF.NbATK,self.ATK.Breakthrought)
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

""".format(self.ATK.Name,self.ATK.HP,self.ATK._Regiment__HP,self.ATK.ORG,self.ATK._Regiment__ORG,
           self.DEF.Name,self.DEF.HP,self.DEF._Regiment__HP,self.DEF.ORG,self.DEF._Regiment__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)
