from W40K_TableValues import *
from W40K_Bonus import *

class Weapon:
    def __init__(self, F=3, PA=None, Range = 24, Cadence = 2, Type="Tir rapide",Quantity=1):
        self.Quantity = Quantity
    # Profils W40K
        self.F = F
        self.PA = PA
        self.Range = Range
        self.Cadence = Cadence
        self.Type = Type
        self.Cadence = 1
        self.Portee = 24
        self.SpecialsRules = []
    # Profils HOI VI
        self.SoftAttack = float()
        self.HardAttack = float()
        self.SoftMeleeAttack = float()
        self.HardMeleeAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.Piercing = float()
        self.HOI4_Profil()
    def HOI4_Profil(self):
        if self.Type == "Melee":
            self.SoftMeleeAttack , self.HardMeleeAttack = 0 , 0
            self.SoftAttack , self.HardAttack = 0 , 0
        else:
            self.SoftMeleeAttack, self.HardMeleeAttack = 0, 0
            self.SoftAttack = SoftAttack_F[self.F]*SoftAttack_PA[self.PA] *self.Quantity
            self.HardAttack = HardAttack_F[self.F]*HardAttack_PA[self.PA] *self.Quantity
        self.Defense = Defense_F[self.F]*Defense_PA[self.PA] *self.Quantity
        self.Breakthrought = Breakthrought_F[self.F]*Breakthrought_PA[self.PA] *self.Quantity
    # Piercing
        self.Piercing = self.F + 4
        if self.PA == 2 : self.Piercing += 1
        if self.PA == 1 : self.Piercing += 2
    # End
        self.Bonus()
    def Bonus(self):
        setWeaponsBonus(self)
    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        Soft Attack   = {}
        Hard Attack   = {}
        Defense       = {}
        Breakthrought = {}
        Piercing      = {}
        """.format(self.SoftAttack,self.HardAttack,
                   self.Defense,self.Breakthrought,
                   self.Piercing)
        print(txt)
    def set_Quantity(self,Quantity):
        self.Quantity = Quantity
        self.HOI4_Profil()


class Upgrade:
    def __init__(self,SA=1,HA=1,SMA=1,HMA=1,DEF=1,BRK=1,Quantity=100):
        """
        type 0.2 for +20% bonus
        """
        self.Quantity = Quantity
        self.SoftAttack_Bonus = SA
        self.HardAttack_Bonus = HA
        self.SoftMeleeAttack_Bonus = SMA
        self.HardMeleeAttack_Bonus = HMA
        self.Defense_Bonus = DEF
        self.Breakthrought_Bonus = BRK