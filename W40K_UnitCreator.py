from W40K_TableValues import *
import numpy as np

class Weapon:
    def __init__(self, F=3, PA=None, Type="Tir rapide",Quantity=1):
        self.Quantity = Quantity
    # Profils W40K
        self.F = F
        self.PA = PA
        self.Type = Type
        self.Cadence = 1
        self.Portee = 24
        self.SpecialsRules = []
    # Profils HOI VI
        self.SoftAttack = float()
        self.HardAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.Piercing = float()
    def HOI4_Profil(self):
        self.SoftAttack = SoftAttack_F[self.F]*SoftAttack_PA[self.PA] *self.Quantity
        self.HardAttack = HardAttack_F[self.F]*HardAttack_PA[self.PA] *self.Quantity
        self.Defense = Defense_F[self.F]*Defense_PA[self.PA] *self.Quantity
        self.Breakthrought = Breakthrought_F[self.F]*Breakthrought_PA[self.PA] *self.Quantity
    # Piercing
        self.Piercing = self.F + 4
        if self.PA == 2 : self.Piercing += 1
        if self.PA == 1 : self.Piercing += 2
        self.Bonus()
    def Bonus(self):
        for rule in self.SpecialsRules:
            if rule == "Perforant":
                self.SoftAttack *= 1.1
                self.HardAttack *= 1.1
                self.Piercing += 1
            if rule == "Fléau de la chair":
                self.SoftAttack *= 1.1
            if rule == "Fléau des chars":
                self.HardAttack *= 1.1
            if rule == "Ignore les couverts":
                self.SoftAttack *= 1.2
            if rule == "Explosion 3'":
                self.SoftAttack *= 1.1
                self.HardAttack += 1.02
            if rule == "Explosion 5'":
                self.SoftAttack *= 1.2
                self.HardAttack += 1.05
        # Type d'armes
        if self.Type == "Lourde":
            self.Defense *= 1.2
        if self.Type == "Assaut":
            self.Breakthrought *= 1.2
        if self.Type == "Tir Rapide": pass
        if self.Type == "Salve":
            self.Defense *= 1.1
            self.Breakthrought = 1.1
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
class Unit:
    def __init__(self,CC=3,CT=3,F=3,E=3,PV=1,A=1,Cd=7,Svg=4,SvgInvu=None,Quantity=1):
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
        self.HP = self.PV*HPbonus_E[self.E] *self.Quantity
        self.ORG = self.Cd *self.Quantity
        self.SoftMeleeAttack = self.A*SoftAttack_CC_CT[self.CC] *self.Quantity
        self.HardMeleeAttack = HMA_SMA_prop[self.F]* self.SoftMeleeAttack* HardAttack_CC_CT[self.CC] *self.Quantity
    # Hardness & Armor
        if self.Svg == 3:
            self.Hardness = 0.1
            self.Armor = 2 * Armor_SvgInvu[self.SvgInvu]
        if self.Svg == 2:
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
        HP            = {}
        ORG           = {}
        Defense       = {}
        Breakthrought = {}
        Piercing      = {}
        """.format(self.HP,self.ORG,
                   self.Defense,self.Breakthrought,
                   self.Piercing)
        print(txt)
    def set_Quantity(self,Quantity):
        self.Quantity = Quantity

class Company:
    def __init__(self):
        self.Unit = Unit()
        self.Equipement = list()
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
    def check_lists(self):
        for el in self.Equipement:
            assert type(el) is Weapon , "Each element of Equipement list must be a :Weapon class:"
    def HOI4_profil(self):
        self.Manpower = self.Unit.Quantity
        self.Quantity_Equipement = np.sum(el.Quantity for el in self.Equipement)
        self.HP = self.Unit.HP
        self.ORG = self.Unit.ORG
        self.SoftAttack = np.sum(el.SoftAttack for el in self.Equipement)
        self.HardAttack = np.sum(el.HardAttack for el in self.Equipement)
        self.SoftMeleeAttack = np.sum(el.SoftMeleeAttack for el in self.Equipement)
        self.HardMeleeAttack = np.sum(el.HardMeleeAttack for el in self.Equipement)
        self.Defense = self.Unit.Defense + np.sum(el.Defense for el in self.Equipement)
        self.Breakthrought = self.Unit.Breakthrought + np.sum(el.Breakthrought for el in self.Equipement)
        self.Hardness = self.Unit.Hardness
        self.Armor = self.Unit.Armor
        self.Piercing = (self.Unit.Piercing + np.sum(el.Quantity*el.Piercing for el in self.Equipement))\
                        /(self.Quantity_Equipement+self.Manpower)
