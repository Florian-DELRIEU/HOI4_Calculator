from W40K_TableValues import *

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
        self.HOI4_Profil()


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
    def round_Stats(self):
        self.Defense = round(self.Defense,2)
        self.Breakthrought = round(self.Breakthrought,2)
        self.SoftAttack = round(self.SoftAttack,2)
        self.HardAttack = round(self.HardAttack,2)
        self.SoftMeleeAttack = round(self.SoftMeleeAttack,2)
        self.HardMeleeAttack = round(self.HardMeleeAttack,2)
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

