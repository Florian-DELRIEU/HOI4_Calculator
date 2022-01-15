from W40K.Functions.Stats_Functions import *
from W40K.Functions.Functions import *
from W40K.Functions.Weapons_bonuses import apply_SpecialsRules,apply_WeaponsType

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
        self.Piercing = float()
        self.Defense_bonus = float(1.0)
        self.Breakthrought_bonus = float(1.0)
        self.HOI4_Profil()

    def HOI4_Profil(self):
    # Cadence
        if self.Type == "Tir rapide":self.Cadence = 2
    # Soft and Hard Attack
        setSA(self)
        setHA(self)
        setSMA(self)
        setHMA(self)
        setPiercing(self)
    # Defense and Break
        apply_WeaponsType(self)
        apply_SpecialsRules(self)
    # End
        round_Stats(self)

    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        Soft Attack   = {}
        Hard Attack   = {}
        Defense       = {}
        Breakthrought = {}
        Piercing      = {}
        """.format(self.SoftAttack,self.HardAttack,
                   self.Defense_bonus,self.Breakthrought_bonus,
                   self.Piercing)
        print(txt)

    def set_Quantity(self,Quantity):
        setQuantity(self, Quantity)

    def isGrenade(self):
        return any(("Grenade" or "grenade") in rule for rule in self.SpecialsRules)

    def __repr__(self):
        return str(self.Quantity) + " " + self.Name

    def __copy__(self, Quantity=None):
        if Quantity is None: Quantity = self.Quantity
        newObject = Weapon()
        for attr in self.__dict__:
            newObject.__setattr__(attr, self.__getattribute__(attr))
        newObject.set_Quantity(Quantity)
        return newObject


class Upgrade:
    def __init__(self,SA=1,HA=1,SMA=1,HMA=1,DEF=1,BRK=1,Quantity=100):
        self.Quantity = Quantity
        self.SoftAttack_Bonus = SA
        self.HardAttack_Bonus = HA
        self.SoftMeleeAttack_Bonus = SMA
        self.HardMeleeAttack_Bonus = HMA
        self.Defense_Bonus = DEF
        self.Breakthrought_Bonus = BRK