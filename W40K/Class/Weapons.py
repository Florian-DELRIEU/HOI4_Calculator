from W40K.FuncAndTables.TableValues import *
from W40K.FuncAndTables.Functions import setWeaponsBonus

class Weapon:
    def __init__(self, F=3, PA=None, Type="Tir rapide", Range = 24, Cadence = 2,Quantity=1,Name="",SpecialsRules=[]):
        self.Quantity = Quantity
    # Profils W40K
        self.F = F
        self.PA = PA
        self.Range = Range
        self.Cadence = Cadence
        self.Type = Type
        self.Name = Name
        self.SpecialsRules = SpecialsRules
    # Profils HOI VI
        self.SoftAttack = float()
        self.HardAttack = float()
        self.SoftMeleeAttack = float()
        self.HardMeleeAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.Piercing = float()
        self.HOI4_Profil()
    def __repr__(self):
        txt = str(self.Quantity) + " " + self.Name
        return txt
    def HOI4_Profil(self):
        if self.Type == "Melee":
            self.SoftMeleeAttack , self.HardMeleeAttack = SoftMeleeAttack_F[self.F] , HardMeleeAttack_F[self.F]
            self.SoftAttack , self.HardAttack = 0 , 0
            self.Cadence = 1
            self.Range = None
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
    def __copy__(self,Quantity):
        NewWeapon = Weapon()
        NewWeapon.F = self.F
        NewWeapon.PA = self.PA
        NewWeapon.Type = self.Type
        NewWeapon.Range = self.Range
        NewWeapon.Name = self.Name
        NewWeapon.Quantity = Quantity
        NewWeapon.HOI4_Profil()
        return NewWeapon


class Upgrade:
    def __init__(self,SA=1,HA=1,SMA=1,HMA=1,DEF=1,BRK=1,Quantity=100):
        self.Quantity = Quantity
        self.SoftAttack_Bonus = SA
        self.HardAttack_Bonus = HA
        self.SoftMeleeAttack_Bonus = SMA
        self.HardMeleeAttack_Bonus = HMA
        self.Defense_Bonus = DEF
        self.Breakthrought_Bonus = BRK