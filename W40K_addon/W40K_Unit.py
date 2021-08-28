from W40K_addon.W40K_TableValues import *
import numpy as np

class Unit:
    def __init__(self,CC=3,CT=3,F=3,E=3,PV=1,A=1,Cd=7,Svg=5,SvgInvu=None,Quantity=1,Type="Infantry",SpecialRules=list,
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
        self.HP = self.PV*HPbonus_E[self.E] *self.Quantity
        self.ORG = self.Cd *self.Quantity
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
        self.Quantity = Quantity
        self.HOI4_Profil()

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
        self.TurretWeapon = list()
        self.HullWeapon = list()
        self.SideWeapon = list()
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
        for weapon in self.HullWeapon:
            weapon.SoftAttack *= 0.33
            weapon.HardAttack *= 0.33
            weapon.Defense *= 0.33
            weapon.Breakthrought *= 0.33
        for weapon in self.SideWeapon:
            weapon.SoftAttack *= 0.66
            weapon.HardAttack *= 0.66
            weapon.Defense *= 0.66
            weapon.Breakthrought *= 0.66
    # Organisation
        if self.Type is "SuperHeavy":   self.ORG = 3
        else:                           self.ORG = 2
        self.ORG *= self.Quantity
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
    def setWeapons(self,TurretList,SideList,HullList):
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
    def set_Quantity(self,Quantity):
        self.Quantity = Quantity
        self.HOI4_Profil()

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
        self.ORG = 1*self.Quantity
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
        self.Quantity = Quantity
        self.HOI4_Profil()