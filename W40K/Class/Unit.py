from W40K.Functions.Stats_Functions import *
from W40K.Functions.Functions import *
from W40K.Functions.Units_bonuses import apply_SpecialRules
import numpy as np
"""
Ensemble des :class: pour Unité terrestre
- :Unit: Infanterie ou Créature Monstrueuse
- :Tank: Vehicule terrestre non marcheurs
- :Walker: Marcheurs
"""

class Infantry:
    def __init__(self,CC=3,CT=3,F=3,E=3,PV=1,A=1,Cd=7,Svg=5,SvgInvu=None,Quantity=1,Type="Infantry",SpecialRules=[],
                 Name = ""):
        """
        Default is Guardsman
        """
        self.Quantity = Quantity
        self.Class = "Infantry"
    # W40K Stats
        self.CC = CC
        self.CT = CT
        self.F = F
        self.E = E
        self.PV = PV
        self.A = A
        self.Cd = Cd
        self.Svg = Svg
        self.SvgInvu = SvgInvu
        self.Type = Type
        self.SpecialRules = SpecialRules
        self.Name = Name
    # HOI Stats
        self.HP = float()
        self.ORG = float()
        self.SoftAttack = float()
        self.HardAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.SoftMeleeAttack = float()
        self.HardMeleeAttack = float()
        self.Hardness = float()
        self.Armor = float()
        self.Piercing = float()
    # Bonus
        self.bonus_CC = np.exp((CC-3)/2.8)
        self.bonus_CT = np.exp((CT-3)/2.8)
        self.HOI4_Profil()
        round_Stats(self)
    def HOI4_Profil(self):
        """
        Determine le profil HOI IV en fonctions des stats W40K
        """
    # Stats
        setHP(self)
        setORG(self)
        setSMA(self)
        setHMA(self)
        setHardness(self)
        setArmor(self)
        setPiercing(self)
        setDefense(self)
        setBreakthrought(self)
    # Bonus
        self.Bonus()
    def Bonus(self):
        apply_SpecialRules(self)
        round_Stats(self)
    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        HP              = {}
        ORG             = {}
        Defense         = {}   
        Breakthrought   = {}
        SoftMA          = {}
        HardMA          = {}
        Hardness        = {}
        Armor           = {}
        """.format(self.HP,self.ORG,
                   self.Defense,self.Breakthrought,
                   self.SoftMeleeAttack,self.HardMeleeAttack,
                   self.Hardness,self.Armor)
        print(txt)
    def __repr__(self):
        return str(self.Quantity) + " " + self.Name
    def set_Quantity(self, Quantity):
        setQuantity(self,Quantity)
    def __copy__(self,Quantity):
        New = Infantry(CT=self.CT,
                       CC=self.CC,
                       F=self.F,
                       Cd=self.Cd,
                       E=self.E,
                       PV = self.PV,
                       A=self.A,
                       Svg=self.Svg,
                       SvgInvu=self.SvgInvu,
                       Name=self.Name,
                       SpecialRules=self.SpecialRules,
                       Type=self.Type,
                       Quantity=1)
        New.HOI4_Profil()
        New.set_Quantity(Quantity)
        return New

########################################################################################################################
########################################################################################################################

class Tank:
    def __init__(self,CT=3,Blind_Av=14,Blind_Side=13,Blind_Arr=10,PC=3,Quantity=1,Type="Heavy",SpecialRules=[],
                 Name= ""):
        """
        Default is Leman Russ battle tank
        """
        self.Quantity = Quantity
        self.Class = "Vehicule"
        self.Name = Name
    # W40K Stats
        self.CT = CT
        self.Blind_Av = Blind_Av
        self.Blind_Side = Blind_Side
        self.Blind_Arr = Blind_Arr
        self.PC = PC
        self.Type = Type
        self.SpecialRules = SpecialRules
        self.TurretWeapon = []
        self.HullWeapon = []
        self.SideWeapon = []
    # HOI Stats
        self.HP = float()
        self.ORG = float()
        self.SoftAttack = float()
        self.HardAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.SoftMeleeAttack = float()
        self.HardMeleeAttack = float()
        self.Hardness = float()
        self.Armor = float()
        self.Piercing = float()
    # Bonus
        self.bonus_CC = 1
        self.bonus_CT = np.exp((CT - 3)/2.8)
        self.HOI4_Profil()
        round_Stats(self)

    def HOI4_Profil(self):
        setHP(self)
        setORG(self)
        setSMA(self)
        setHMA(self)
        # Hardness & Armor
        setHardness(self)
        setArmor(self)
        # Piercing
        setPiercing(self)
        # Defense & Breakthrought
        setDefense(self)
        setBreakthrought(self)
    # Bonus
        self.Bonus()
        round_Stats(self)

    def __repr__(self):
            return str(self.Quantity) + " " + self.Name

    def Bonus(self):
        apply_SpecialRules(self)
        round_Stats(self)

    def setWeapons(self,TurretList=[],SideList=[],HullList=[]):
        self.TurretWeapon = TurretList  # first Turret weapon considered as Main gun
        self.SideWeapon = SideList
        self.HullWeapon = HullList
        self._setTankType()
        self._setWeapons()
        round_Stats(self)

    def _setTankType(self):
        if len(self.TurretWeapon) == 0: # if any turret weapon
            if len(self.HullWeapon) != 0: # and have hull weapons
                self.Type += " Destroyer"
            elif len(self.SideWeapon) != 0: # if not hull weapons, have sides weapons ??
                self.Type += " Defender"
        elif self.TurretWeapon[0].Type == "Ordnance" and self.Type != "Heavy":
            self.Type += " SP Artillery"                # set tank type as SP artillery
    def _setWeapons(self):
        """
        FIXME
            - Le basilisk perd tout ses valeurs Defense/Breakthrought a cause de cette fonction
            - breakpoint: self.Name == "Basilisk"
        """
        for weapon in self.TurretWeapon+self.HullWeapon+self.SideWeapon:
            weapon.Defense_bonus = 1
            weapon.Breakthrought_bonus = 1
        if len(self.TurretWeapon) == 0 and len(self.HullWeapon) != 0:
            self.Breakthrought *= 0.8
            self.Defense *= 1.2
        if len(self.HullWeapon) != 0:
            for weapon in self.HullWeapon:
                weapon.SoftAttack *= 0.33
                weapon.HardAttack *= 0.33
        if len(self.SideWeapon) != 0:
            for weapon in self.SideWeapon:
                weapon.SoftAttack *= 0.66
                weapon.HardAttack *= 0.66
        self.SoftAttack = np.sum([el.SoftAttack for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.HardAttack = np.sum([el.HardAttack for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.Defense *= np.prod([el.Defense_bonus for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.Breakthrought = np.sum([el.Breakthrought_bonus for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.Piercing = np.max([weapon.Piercing for weapon in self.TurretWeapon+self.HullWeapon+self.SideWeapon])
    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        HP              = {}
        ORG             = {}
        Defense         = {}   
        Breakthrought   = {}
        SoftMA          = {}
        HardMA          = {}
        Hardness        = {}
        Armor           = {}
        """.format(self.HP,self.ORG,
                   self.Defense,self.Breakthrought,
                   self.SoftMeleeAttack,self.HardMeleeAttack,
                   self.Hardness,self.Armor)
        print(txt)
    def set_Quantity(self,Quantity):
        setQuantity(self, Quantity)
    def __copy__(self,Quantity=None):
        if Quantity is None: Quantity = self.Quantity
        newObject = Tank()
        for attr in self.__dict__:
            newObject.__setattr__(attr, self.__getattribute__(attr))
        newObject.set_Quantity(Quantity)
        return newObject

########################################################################################################################
########################################################################################################################

class Walker:
    def __init__(self,CC=3,CT=3,F=5,Blind_Av=12,Blind_Side=10,Blind_Arr=10,A=1,PC=2,Quantity=1,Type="Walker"
                 ,SpecialRules=list,Name = ""):
        """
        Default is Sentinel
        """
        self.Quantity = Quantity
        self.Class = "Vehicule"
        self.Name = Name
    # W40K Stats
        self.CC = CC
        self.CT = CT
        self.F = F
        self.Blind_Av = Blind_Av
        self.Blind_Side = Blind_Side
        self.Blind_Arr = Blind_Arr
        self.A = A
        self.PC = PC
        self.Type = Type
        self.SpecialRules = SpecialRules
        # HOI Stats
        self.HP = float()
        self.ORG = float()
        self.SoftAttack = float()
        self.HardAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.SoftMeleeAttack = float()
        self.HardMeleeAttack = float()
        self.Hardness = float()
        self.Armor = float()
        self.Piercing = float()
    # Bonus
        self.bonus_CC = np.exp((CC - 3)/2.8)
        self.bonus_CT = np.exp((CT - 3)/2.8)
        self.HOI4_Profil()
        round_Stats(self)
    def HOI4_Profil(self):
        setHP(self)*self.Quantity
        setORG(self)
        setSMA(self)*self.Quantity
        setHMA(self)*self.Quantity
        # Hardness & Armor
        setHardness(self)
        setArmor(self)
        # Piercing
        setPiercing(self)
        # Defense & Breakthrought
        setDefense(self)
        setBreakthrought(self)
        self.Bonus()
        # End

    def Bonus(self):
        apply_SpecialRules(self)
        round_Stats(self)

    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        HP              = {}
        ORG             = {}
        Defense         = {}   
        Breakthrought   = {}
        SoftMA          = {}
        HardMA          = {}
        Hardness        = {}
        Armor           = {}
        """.format(self.HP,self.ORG,
                   self.Defense,self.Breakthrought,
                   self.SoftMeleeAttack,self.HardMeleeAttack,
                   self.Hardness,self.Armor)
        print(txt)

    def __repr__(self):
        return str(self.Quantity) + " " + self.Name

    def set_Quantity(self,Quantity):
        setQuantity(self, Quantity)

    def __copy__(self, Quantity=None):
        if Quantity is None: Quantity = self.Quantity
        newObject = Walker()
        for attr in self.__dict__:
            newObject.__setattr__(attr, self.__getattribute__(attr))
        newObject.set_Quantity(Quantity)
        return newObject