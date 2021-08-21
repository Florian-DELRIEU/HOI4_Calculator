from W40K_TableValues import *
from W40K_Weapons import *
from W40K_Unit import *
import numpy as np

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
        self.HOI4_Profil()
    def check_lists(self):
        for el in self.Equipement:
            assert type(el) is Weapon , "Each element of Equipement list must be a :Weapon class:"
    def HOI4_Profil(self):
        self.Manpower = self.Unit.Quantity
        self.Quantity_Equipement = np.sum([el.Quantity for el in self.Equipement])
        self.HP = self.Unit.HP
        self.ORG = self.Unit.ORG
        self.SoftAttack = np.sum([el.SoftAttack for el in self.Equipement])
        self.HardAttack = np.sum([el.HardAttack for el in self.Equipement])
        self.SoftMeleeAttack = np.sum([el.SoftMeleeAttack for el in self.Equipement])
        self.HardMeleeAttack = np.sum([el.HardMeleeAttack for el in self.Equipement])
        self.Defense = self.Unit.Defense + np.sum([el.Defense for el in self.Equipement])
        self.Breakthrought = self.Unit.Breakthrought + np.sum([el.Breakthrought for el in self.Equipement])
        self.Hardness = self.Unit.Hardness
        self.Armor = self.Unit.Armor
        self.Piercing = (self.Unit.Piercing + np.sum([el.Quantity*el.Piercing for el in self.Equipement]))\
                        /(self.Quantity_Equipement+self.Manpower)
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