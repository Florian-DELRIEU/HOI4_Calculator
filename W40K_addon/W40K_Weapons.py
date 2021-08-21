from W40K_TableValues import *

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