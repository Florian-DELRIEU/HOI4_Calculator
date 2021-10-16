from W40K.Functions.Stats_Functions import *
from W40K.Functions.Functions import *

class Weapon:
    def __init__(self, F=3, PA=None, Range = 24, Type="Tir rapide", Cadence = 1,Quantity=1,SpecialsRules=[],Name=""):
        self.Quantity = Quantity
        self.Class = "Weapon"
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
    # Cadence
        if self.Type == "Tir rapide":self.Cadence = 2
        setSA(self)
        setHA(self)
        setSMA(self)
        setHMA(self)
        setDefense(self)
        setBreakthrought(self)
        setPiercing(self)
    # End
        self.Bonus()
        round_Stats(self)
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
        setQuantity(self, Quantity)
    def __copy__(self,Quantity):
        NewWeapon = Weapon()
        NewWeapon.F = self.F
        NewWeapon.PA = self.PA
        NewWeapon.Type = self.Type
        NewWeapon.Range = self.Range
        NewWeapon.Name = self.Name
        NewWeapon.SpecialsRules = self.SpecialsRules
        NewWeapon.HOI4_Profil()
        NewWeapon.set_Quantity(Quantity)
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