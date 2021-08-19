from W40K_TableValues import *

class Weapons:
    def __init__(self):
    # Profils W40K
        self.F = 3
        self.PA = None
        self.Type = "Tir rapide"
        self.Cadence = 1
        self.Portee = 24
    # Profils HOI VI
        self.SoftAttack = float()
        self.HardAttack = float()
        self.Defense = float()
        self.Breakthrought = float()
        self.Piercing = float()
    def HOI4_Profil(self):
        self.SoftAttack = SoftAttack_F(self.F)*SoftAttack_PA(self.PA)
        self.HardAttack = HardAttack_F(self.F)*HardAttack_PA(self.PA)
        self.Defense = Defense_F(self.F)*Defense_PA(self.PA)
        self.Breakthrought = Breakthrought_F(self.F)*Breakthrought_PA(self.PA)
        self.Piercing = self.F + 4
