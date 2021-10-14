from MyPack.Utilities import *
from W40K.Functions.Functions import *
from W40K.Functions.TableValues import *

class Company:
    def __init__(self,Unit=None,Equipement=[]):
        self.Unit = Unit
        self.Equipement = Equipement
        self.Upgrade = list()
        self.Manpower = float()
        self.Quantity_Equipement = float()
    # HOI Stats
        self.HP = float()
        self.ORG = float()
        self.SoftAttack = float()
        self.SoftMeleeAttack = float()
        self.HardAttack = float()
        self.HardMeleeAttack = float()
        self.Hardness = float()
        self.Armor = float()
        self.Piercing = float()
        self.Breakthrought = float()
        self.Defense = float()
        self.HOI4_Profil()
    def HOI4_Profil(self):
        if self.Unit is None:
            pass
        else:
            self.Manpower = self.Unit.Quantity
            self.Quantity_Equipement = np.sum([el.Quantity for el in self.Equipement])
            self.HP = self.Unit.HP
            self.ORG = self.Unit.ORG
            self.SoftAttack = np.sum([el.SoftAttack for el in self.Equipement])*SoftAttack_CC_CT[self.Unit.CT]
            self.HardAttack = np.sum([el.HardAttack for el in self.Equipement])*HardAttack_CC_CT[self.Unit.CT]
            self.SoftMeleeAttack = np.sum([el.SoftMeleeAttack for el in self.Equipement])*SoftAttack_CC_CT[self.Unit.CC]\
                                   + self.Unit.SoftMeleeAttack
            self.HardMeleeAttack = np.sum([el.HardMeleeAttack for el in self.Equipement])*HardAttack_CC_CT[self.Unit.CC]\
                                   + self.Unit.HardMeleeAttack
            self.Defense = self.Unit.Defense + np.sum([el.Defense for el in self.Equipement])
            self.Breakthrought = self.Unit.Breakthrought + np.sum([el.Breakthrought for el in self.Equipement])
            self.Hardness = self.Unit.Hardness
            self.Armor = self.Unit.Armor
            self.Piercing = (self.Unit.Piercing + np.sum([el.Quantity*el.Piercing for el in self.Equipement]))\
                            /(self.Quantity_Equipement+self.Manpower)
        # End
        round_Stats(self)
    def setUnit(self,Unit):
        self.Unit = Unit
        self.HOI4_Profil()
    def setEquipement(self,List=list):
        self.Equipement = List
        self.HOI4_Profil()
    def setUpgrade(self,List=list):
        self.Upgrade = List
        setUpgradeBonus(self)
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

class Regiment:
    def __init__(self,CompagnieList=[],Name=""):
        self.Companies = CompagnieList
        self.Name = Name
    # Stats when stregth == 1
        self.__HP = float()
        self.__ORG = float()
        self.__SoftAttack = float()
        self.__SoftMeleeAttack = float()
        self.__HardAttack = float()
        self.__HardMeleeAttack = float()
        self.Hardness = float()
        self.Armor = float()
        self.Piercing = float()
        self.__Breakthrought = float()
        self.__Defense = float()
    # Current Stats
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
        self.NbATK = float()
        self.isDefending = True
        self.set_STR()
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
        self.Armor = np.mean([el.Armor for el in self.Companies])
        self.Piercing = np.mean([el.Piercing for el in self.Companies])
        self.__Breakthrought = np.sum([el.Breakthrought for el in self.Companies])
        self.__Defense = np.sum([el.Defense for el in self.Companies])
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
        self.NbATK /= 10  # les attaques sont divisé par 10 (voir wiki)
        round_Stats(self)
    def Damage(self,Striker):
        """
        Calcul du nombre de touche et des dégats
        :param Striker: Division attaquante
        """
        self.set_STR() # MAJ
        NbDAMAGE = Striker.NbATK #Recupere le nombre d'attaque de l'attaquant
    # Attaquant ou defenseur ?
        if self.isDefending: DEF = self.Defense         # Si defend alors utilise DEFENSE stat
        else:                DEF = self.Breakthrought   # si attaque alors utilise BREAKTOUGHT stat
    # Defense de la cible
        if DEF > NbDAMAGE: NbDAMAGE *= 0.1
        else:              NbDAMAGE = self.Defense*0.1 + (NbDAMAGE-self.Defense)*0.4
    # Arrondissement des dégats
        round_Stats(self)
    # Calcul des dégats entre les PV et l'ORG
    # PV Dégats
        self.HP -= 1.5*NbDAMAGE # Moyenne de D2
        self.HP = truncDecimal(self.HP,1)
        if self.HP <= 0 : self.HP = 0
    # ORG Dégats
        if self.Piercing < Striker.Armor:
            self.ORG -= 3.5*NbDAMAGE # Moyenne de D6
        else:
            self.ORG -= 2.5*NbDAMAGE # Moyenne de D4
        self.ORG = truncDecimal(self.ORG,1)
        if self.ORG <= 0 : self.ORG = 0
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