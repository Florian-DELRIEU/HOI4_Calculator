from W40K_TableValues import *
from W40K_Weapons import *
from W40K_Unit import *
import numpy as np

class Company:
    def __init__(self):
        self.Unit = None
        self.Equipement = list()
        self.Upgrade = list()
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
        self.HOI4_Profil()
    def check_lists(self):
        for el in self.Equipement:
            assert type(el) is Weapon , "Each element of Equipement list must be a :Weapon class:"
    def HOI4_Profil(self):
        if self.Unit is None:
            pass
        else:
            self.Manpower = self.Unit.Quantity
            self.Quantity_Equipement = np.sum([el.Quantity for el in self.Equipement])
            self.HP = self.Unit.HP
            self.ORG = self.Unit.ORG
            self.SoftAttack = np.sum([el.SoftAttack for el in self.Equipement])*SoftAttack_CC_CT[self.Unit.CT]
            self.HardAttack = np.sum([el.HardAttack for el in self.Equipement])*HardAttack_CC_CT[self.Unit.CT]
            self.SoftMeleeAttack = np.sum([el.SoftMeleeAttack for el in self.Equipement])*SoftAttack_CC_CT[self.Unit.CC]\
                                   + self.Unit.SoftMeleeAttack
            self.HardMeleeAttack = np.sum([el.HardMeleeAttack for el in self.Equipement])*HardAttack_CC_CT[self.Unit.CC]\
                                   + self.Unit.HardMeleeAttack
            self.Defense = self.Unit.Defense + np.sum([el.Defense for el in self.Equipement])
            self.Breakthrought = self.Unit.Breakthrought + np.sum([el.Breakthrought for el in self.Equipement])
            self.Hardness = self.Unit.Hardness
            self.Armor = self.Unit.Armor
            self.Piercing = (self.Unit.Piercing + np.sum([el.Quantity*el.Piercing for el in self.Equipement]))\
                            /(self.Quantity_Equipement+self.Manpower)
        # End
        self.round_Stats()
    def round_Stats(self):
        self.Defense = round(self.Defense,2)
        self.Breakthrought = round(self.Breakthrought,2)
        self.SoftAttack = round(self.SoftAttack,2)
        self.HardAttack = round(self.HardAttack,2)
        self.SoftMeleeAttack = round(self.SoftMeleeAttack,2)
        self.HardMeleeAttack = round(self.HardMeleeAttack,2)
    def setUnit(self,Unit):
        self.Unit = Unit
        self.HOI4_Profil()
    def setEquipement(self,List=list):
        self.Equipement = List
        self.HOI4_Profil()
    def Show_HOI_Stats(self):
        self.HOI4_Profil()
        txt = """
        HP              = {}
        ORG             = {}
        Defense         = {}   
        Breakthrought   = {}
        SoftAttack      = {}
        HardAttack      = {}
        SoftMA          = {}
        HardMA          = {}
        Hardness        = {}
        Armor           = {}
        """.format(self.HP, self.ORG,
                   self.Defense, self.Breakthrought,
                   self.SoftAttack, self.HardAttack,
                   self.SoftMeleeAttack, self.HardMeleeAttack,
                   self.Hardness, self.Armor)
        print(txt)