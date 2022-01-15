from MyPack2.Utilities import *
from W40K.Functions.Functions import *
#from W40K.Functions.Stats_Functions import bonus_CC,bonus_CT
from W40K.Functions.Upgrades_bonuses import setUpgradeBonus

class Company:
    def __init__(self,Unit=None,Equipement=None):
        self.Unit = Unit
        self.Class = "Company"
        self.Type = ""
        self.Equipement = [] if Equipement is None else Equipement
        self.Upgrade = []
        self.Manpower = float()
        self.Quantity_Equipement = float()
        self.BRK_bonus = 1
        self.DEF_bonus = 1
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
        self.Width = float()
        self.HOI4_Profil()
    def HOI4_Profil(self):
        if self.Unit is not None:
        # TYPE
            self.Type = self.Unit.Class
        # MANPOWER & EQUIPEMENT
            self.Manpower = self.Unit.Quantity
            self.Quantity_Equipement = np.sum([el.Quantity for el in self.Equipement])
        # HEALTH
            self.HP = self.Unit.HP
            self.ORG = self.Unit.ORG
        # ATTACK
            self.SoftAttack = (self.Unit.SoftAttack + np.sum([el.SoftAttack for el in self.Equipement]))\
                                                                                *self.Unit.bonus_CT
            self.HardAttack = (self.Unit.HardAttack + np.sum([el.HardAttack for el in self.Equipement])) \
                                                                                *self.Unit.bonus_CT
            self.SoftMeleeAttack = np.sum([el.SoftMeleeAttack for el in self.Equipement])*self.Unit.bonus_CC\
                                                                                + self.Unit.SoftMeleeAttack
            self.HardMeleeAttack = np.sum([el.HardMeleeAttack for el in self.Equipement])*self.Unit.bonus_CC\
                                                                                + self.Unit.HardMeleeAttack
            self.Piercing = (self.Unit.Piercing + np.sum([el.Quantity*el.Piercing for el in self.Equipement]))\
                            /(self.Quantity_Equipement+self.Manpower)
        # DEFENSE
            self.set_Defense_bonuses()
            self.set_Breakthrought_bonuses()
            self.Defense = self.Unit.Defense
            self.Breakthrought = self.Unit.Breakthrought
            self.Hardness = self.Unit.Hardness
            self.Armor = self.Unit.Armor
        # End
        round_Stats(self)

    def set_Defense_bonuses(self):
        MANPOWER = self.Manpower
        DEF_bonus = 1
        for weapon in self.Equipement:
            current_DEF_bonus = weapon.Defense_bonus
            current_equip_ratio = weapon.Quantity / MANPOWER
            current_DEF_bonus *= current_equip_ratio
            DEF_bonus *= current_DEF_bonus
        self.Unit.Defense *= DEF_bonus

    def set_Breakthrought_bonuses(self):
        MANPOWER = self.Manpower
        BRK_bonus = 1
        for weapon in self.Equipement:
            current_BRK_bonus = weapon.Breakthrought_bonus
            current_equip_ratio = weapon.Quantity / MANPOWER
            current_BRK_bonus *= current_equip_ratio
            BRK_bonus *= current_BRK_bonus
        self.Unit.Breakthrought *= BRK_bonus

    def setUnit(self,Unit):
        self.Unit = Unit
        self.HOI4_Profil()

    def setEquipement(self,List:list):
        self.Equipement = List
        self.HOI4_Profil()

    def setUpgrade(self,List:list):
        self.Upgrade = List
        setUpgradeBonus(self)

    def setWidth(self):
        if   self.Type == "Infantry":   self.Width = 2
        elif self.Type == "Tank":       self.Width = 2
        elif self.Type == "Artillery":  self.Width = 3
        else:                           self.Width = 0

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

