import numpy as np
from MyPack2.Utilities import truncDecimal
from W40K.Functions.Functions import round_Stats
from W40K.Functions.Leader_func import set_LeaderSkills

class Regiment:
    def __init__(self,CompagnieList=[],XP=0,Entrenchment_level=0,Name=""):
        self.Companies = CompagnieList
        self.Name = Name
    # Stats when stregth == 1
        self.__HP = float()
        self.__ORG = float()
        self.__SoftAttack = float()
        self.__SoftMeleeAttack = float()
        self.__HardAttack = float()
        self.__HardMeleeAttack = float()
        self.__Breakthrought = float()
        self.__Defense = float()
        self.Armor = float()
        self.Piercing = float()
        self.Hardness = float()
    # Current Stats
        self.Experience = XP
        self.Entrenchment = Entrenchment_level
        self.Strength = 1
        self.SoftAttack = float()
        self.SoftMeleeAttack = float()
        self.HardAttack = float()
        self.HardMeleeAttack = float()
        self.Breakthrought = float()
        self.Defense = float()
        self.HOI4_Profil()
        self.HP = self.__HP
        self.ORG = self.__ORG
    # Battle
        self.Width = float()
        self.NbATK = float()
        self.isDefending = True
        self.set_STR()
        round_Stats(self)

    def __repr__(self):
        return self.Name

    def setCompanies(self,CompaniesList=[]):
        self.Companies = CompaniesList
        self.HOI4_Profil()

    def HOI4_Profil(self):
    # Default Stats
        self.__HP = np.sum([el.HP for el in self.Companies])
        self.__ORG = np.mean([el.ORG for el in self.Companies])
        self.__SoftAttack = np.sum([el.SoftAttack for el in self.Companies])
        self.__SoftMeleeAttack = np.sum([el.SoftMeleeAttack for el in self.Companies])
        self.__HardAttack = np.sum([el.HardAttack for el in self.Companies])
        self.__HardMeleeAttack = np.sum([el.HardMeleeAttack for el in self.Companies])
        self.Hardness = np.mean([el.Hardness for el in self.Companies])
        self.Armor = 0.7*np.mean([el.Armor for el in self.Companies]) + 0.3*np.max([el.Armor for el in self.Companies])
        self.Piercing = 0.7*np.mean([el.Piercing for el in self.Companies]) + 0.3*np.max([el.Piercing for el in self.Companies])
        self.__Breakthrought = np.sum([el.Breakthrought for el in self.Companies])
        self.__Defense = np.sum([el.Defense for el in self.Companies])
        self.Width = np.sum([el.Width for el in self.Companies])
        self.apply_bonuses()

    def apply_bonuses(self):
        """Regroupe toutes les fonctions donnant des bonuses aux stats des R??giments"""
        self.set_XP()
        self.set_Entrenchment()

    def set_XP(self):  # sourcery skip: flip-comparison
        XP = self.Experience
        if   0  <= XP < 10: Land_modificator = 0.75
        elif 10 <= XP < 30: Land_modificator = 1
        elif 30 <= XP < 75: Land_modificator = 1.25
        elif 75 <= XP < 90: Land_modificator = 0.50
        elif 90 <= XP     : Land_modificator = 1.75
        else:               Land_modificator = 1
        self.__SoftAttack *= Land_modificator
        self.__HardAttack *= Land_modificator
        self.__SoftMeleeAttack *= Land_modificator
        self.__HardMeleeAttack *= Land_modificator
        self.__Breakthrought *= Land_modificator
        self.__Defense *= Land_modificator

    def set_Entrenchment(self):
        self.__Defense *= 1.02**(self.Entrenchment)
        self.__SoftAttack *= 1.02**(self.Entrenchment)
        self.__HardAttack *= 1.02**(self.Entrenchment)

    def set_STR(self):
        self.Strength = self.HP / self.__HP
    # Maj des stats
        self.SoftAttack = self.__SoftAttack * self.Strength
        self.HardAttack = self.__HardAttack * self.Strength
        self.SoftMeleeAttack = self.__SoftMeleeAttack * self.Strength
        self.HardMeleeAttack = self.__HardMeleeAttack * self.Strength
        self.Breakthrought = self.__Breakthrought * self.Strength
        self.Defense = self.__Defense * self.Strength

    def Attaque(self,Target,CAC_level):
        assert type(Target) == Regiment
        self.set_STR()
        NbRangeATK = Target.Hardness*self.HardAttack + (1 - Target.Hardness)*self.SoftAttack  # Calcul du nbr d'attaque en fonction du Hardness
        NbMeleeATK = Target.Hardness*self.HardMeleeAttack + (1 - Target.Hardness)*self.SoftMeleeAttack
        NbATK = NbMeleeATK*CAC_level + NbRangeATK
        # Piercing ?
        if self.Piercing <= Target.Armor:
            NbATK /= 2  # si perce pas
        else:
            self.NbATK = NbATK  # si perce
        self.NbATK /= 10  # les attaques sont divis?? par 10 (voir wiki)
        round_Stats(self)

    def Damage(self,Striker):
        """
        Calcul du nombre de touche et des d??gats
        :param Striker: Division attaquante
        """
        self.set_STR() # MAJ
        NbDAMAGE = Striker.NbATK #Recupere le nombre d'attaque de l'attaquant
    # Attaquant ou defenseur ?
        DEF = self.Defense/10 if self.isDefending else self.Breakthrought/10
    # Defense de la cible
        if DEF > NbDAMAGE: NbDAMAGE *= 0.1
        else:              NbDAMAGE = DEF*0.1 + (NbDAMAGE-DEF)*0.4
    # Arrondissement des d??gats
        round_Stats(self)
    # Calcul des d??gats entre les PV et l'ORG
    # PV D??gats
        self.HP -= 1.5*NbDAMAGE # Moyenne de D2
        self.HP = truncDecimal(self.HP,1)
        self.HP = max(self.HP, 0)
    # ORG D??gats
        self.ORG -= 3.5*NbDAMAGE if self.Piercing < Striker.Armor else 2.5*NbDAMAGE
        self.ORG = truncDecimal(self.ORG,1)
        self.ORG = max(self.ORG, 0)

    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        HP              = {}
        ORG             = {}
        Defense         = {}   
        Breakthrought   = {}
        SoftAttack      = {}
        HardAttack      = {}
        SoftMA          = {}
        HardMA          = {}
        Hardness        = {}
        Armor           = {}
        """.format(self.HP, self.ORG,
                   self.Defense, self.Breakthrought,
                   self.SoftAttack, self.HardAttack,
                   self.SoftMeleeAttack, self.HardMeleeAttack,
                   self.Hardness, self.Armor)
        print(txt)