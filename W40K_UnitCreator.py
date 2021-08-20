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
        self.Quantity = Quantity
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
    def __init__(self,CC,CT,F,E,PV,A,Cd,Svg):
    # W40K Stats
        self.CC = CC
        self.CT = CT
        self.F = F
        self.E = E
        self.PV = PV
        self.A = A
        self.Cd = Cd
        self.Svg = Svg
    # HOI Stats
        self.HP = float()
        self.ORG = float()
        self.SoftAttack = float()
        self.HardAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.MeleeAttack = float()
        self.Hardness = float()
        self.Armor = float()
        self.Piercing = float()

