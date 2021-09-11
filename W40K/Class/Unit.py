from W40K.Class.FuncAndTables.TableValues import *
from W40K.Class.FuncAndTables.Functions import *
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
        self.HOI4_Profil()
    def HOI4_Profil(self):
        """
        Determine le profil HOI IV en fonctions des stats W40K
        """
        self.HP = self.PV*HPbonus_E[self.E] *self.Quantity
        self.ORG = self.Cd * 10
        self.SoftMeleeAttack = self.A*SoftAttack_CC_CT[self.CC] *self.Quantity
        self.HardMeleeAttack = HMA_SMA_prop[self.F]* self.SoftMeleeAttack* HardAttack_CC_CT[self.CC]
    # Hardness & Armor
        if self.Svg == 3:
            self.Hardness = 0.1
            self.Armor = 2 * Armor_SvgInvu[self.SvgInvu]
        elif self.Svg == 2:
            self.Hardness = 0.2
            self.Armor = 4 * Armor_SvgInvu[self.SvgInvu]
        else:
            self.Hardness = 0.0
            self.Armor = 0 * Armor_SvgInvu[self.SvgInvu]
    # Piercing
        self.Piercing = self.F+4
    # Defense & Breakthrought
        self.Defense = Defense_F[self.F] *self.Quantity
        self.Breakthrought = Breakthrought_F[self.F] *self.Quantity
        if self.Svg == 5:
            self.Defense *= 0.9
            self.Breakthrought *= 0.9
        if self.Svg == 6:
            self.Defense *= 0.8
            self.Breakthrought *= 0.8
        if self.Svg is None:
            self.Defense *= 0.7
            self.Breakthrought *= 0.7
        setUnitBonus(self)
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
        txt = str(self.Quantity) + " " + self.Name
        return txt
    def set_Quantity(self,Quantity):
        set_Quantity(self,Quantity)
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
                       Quantity=Quantity)
        New.HOI4_Profil()
        return New

########################################################################################################################
########################################################################################################################

class Tank:
    def __init__(self,CT=3,Blind_Av=14,Blind_Side=13,Blind_Arr=10,PC=3,Quantity=1,Type="Heavy Tank",SpecialRules=list):
        """
        Default is Leman Russ battle tank
        """
        self.Quantity = Quantity
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
        self.HOI4_Profil()
    def HOI4_Profil(self):
        self.HP = self.PC * self.Quantity
        if self.Type == "Chariot":
            self.SoftMeleeAttack = 0.5
            self.HardMeleeAttack = 0.1
            self.Defense = 1
            self.Breakthrought = 0.5
        if self.Type == "Tank":
            self.SoftMeleeAttack = 1
            self.HardMeleeAttack = 0.5
            self.Defense = 1.5
            self.Breakthrought = 1
        if self.Type == "Heavy":
            self.SoftMeleeAttack = 1.2
            self.HardMeleeAttack = 1.5
            self.Defense = 3
            self.Breakthrought = 1.5
        if self.Type == "SuperHeavy":
            self.SoftMeleeAttack = 1.4
            self.HardMeleeAttack = 2
            self.Defense = 5
            self.Breakthrought = 2
        if len(self.HullWeapon) != 0:
            for weapon in self.HullWeapon:
                weapon.SoftAttack *= 0.33
                weapon.HardAttack *= 0.33
                weapon.Defense *= 0.33
                weapon.Breakthrought *= 0.33
        if len(self.SideWeapon) != 0:
            for weapon in self.SideWeapon:
                weapon.SoftAttack *= 0.66
                weapon.HardAttack *= 0.66
                weapon.Defense *= 0.66
                weapon.Breakthrought *= 0.66
        self.SoftAttack = np.sum([el.SoftAttack for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.HardAttack = np.sum([el.HardAttack for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.Defense = np.sum([el.Defense for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
        self.Breakthrought = np.sum([el.Breakthrought for el in self.HullWeapon+self.TurretWeapon+self.SideWeapon])
    # Organisation
        if self.Type == "SuperHeavy":   self.ORG = 30
        else:                           self.ORG = 20
    # Hardness
        if self.Type == "Chariot":      self.Hardness = 0.80
        elif self.Type == "Tank":       self.Hardness = 0.90
        elif self.Type == "Heavy":      self.Hardness = 0.95
        elif self.Type == "SuperHeavy": self.Hardness = 0.99
        else:                           pass
        if self.Type == "Oppen-Topped": self.Hardness -= 0.1
        if self.Hardness <= 0: self.Hardness = 0
        if self.Hardness >= 1: self.Hardness = 1
    # Armor
        self.Armor = np.mean((self.Blind_Av,self.Blind_Side,self.Blind_Arr))
    def setWeapons(self,TurretList=[],SideList=[],HullList=[]):
        self.TurretWeapon = TurretList
        self.SideWeapon = SideList
        self.HullWeapon = HullList
        self.HOI4_Profil()
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
    def set_Quantity(self,Quantity): set_Quantity(self,Quantity)
    def __copy__(self,Quantity=None):
        if Quantity==None: Quantity = self.Quantity
        New = Tank(CT=self.CT,
                   Blind_Av=self.Blind_Av,
                   Blind_Side=self.Blind_Side,
                   Blind_Arr=self.Blind_Arr,
                   PC = self.PC,
                   SpecialRules=self.SpecialRules,
                   Type=self.Type,
                   Quantity=Quantity)
        New.HOI4_Profil()
        return New

########################################################################################################################
########################################################################################################################

class Walker:
    def __init__(self,CC=3,CT=3,F=5,Blind_Av=12,Blind_Side=10,Blind_Arr=10,A=1,PC=2,Quantity=1,Type="Marcheur"
                 ,SpecialRules=list):
        """
        Default is Sentinel
        """
        self.Quantity = Quantity
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
    def HOI4_Profil(self):
        self.HP = self.PC * self.Quantity
        self.ORG = 10
        self.SoftMeleeAttack = self.A*SoftAttack_CC_CT[self.CC]*self.Quantity
        self.HardMeleeAttack = HMA_SMA_prop[self.F]*self.SoftMeleeAttack*HardAttack_CC_CT[self.CC]*self.Quantity
    # Piercing
        self.Piercing = self.F + 4
    # Defense & Breakthrought
        self.Defense = Defense_F[self.F]*self.Quantity
        self.Breakthrought = Breakthrought_F[self.F]*self.Quantity
    # Hardness & Armor
        self.Armor = np.mean(self.Blind_Av,self.Blind_Side,self.Blind_Arr)
        self.Hardness = 0.7
    # End
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
        set_Quantity(self,Quantity)
    def __copy__(self,Quantity):
        New = Walker(CT=self.CT,
                     CC=self.CC,
                     Blind_Av=self.Blind_Av,
                     Blind_Side=self.Blind_Side,
                     Blind_Arr=self.Blind_Arr,
                     PC = self.PC,
                     A=self.A,
                     SpecialRules=self.SpecialRules,
                     Type=self.Type,
                     Quantity=Quantity)
        New.HOI4_Profil()
        return New