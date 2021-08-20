from W40K_TableValues import *

class Weapons:
    def __init__(self, F=3, PA=None, Type="Tir rapide"):
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
        self.SoftAttack = SoftAttack_F[self.F]*SoftAttack_PA[self.PA]
        self.HardAttack = HardAttack_F[self.F]*HardAttack_PA[self.PA]
        self.Defense = Defense_F[self.F]*Defense_PA[self.PA]
        self.Breakthrought = Breakthrought_F[self.F]*Breakthrought_PA[self.PA]
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

class Unit:
    def __init__(self,CC=3,CT=3,F=3,E=3,PV=1,A=1,Cd=7,Svg=4,SvgInvu=None):
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
        self.HP = self.PV*HPbonus_E[self.E]
        self.ORG = self.Cd
        self.SoftMeleeAttack = self.A*SoftAttack_CC_CT[self.CC]
        self.HardMeleeAttack = HMA_SMA_prop[self.F]*self.SoftMeleeAttack*HardAttack_CC_CT[self.CC]
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
        self.Defense = Defense_F[self.F]
        self.Breakthrought = Breakthrought_F[self.F]
        if self.Svg == 5:
            self.Defense *= 0.9
            self.Breakthrought *= 0.9
        if self.Svg == 6:
            self.Defense *= 0.8
            self.Breakthrought *= 0.8
        if self.Svg is None:
            self.Defense *= 0.7
            self.Breakthrought *= 0.7
