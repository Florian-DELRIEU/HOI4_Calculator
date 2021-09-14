def setWeaponsBonus(Object):
    """
    Verifie les règles spéciales des :class Weapons: pour ajouté les bonus
    :param Object: class weapons
    """
    #assert type(Object) == Weapon , "Object must be :class Weapon:"
# Weapons Specials rules
    for rule in Object.SpecialsRules:
        if rule == "Perforant":
            Object.SoftAttack *= 1.1
            Object.HardAttack *= 1.1
            Object.Piercing += 1
        if rule == "Fléau de la chair":
            Object.SoftAttack *= 1.1
        if rule == "Fléau des chars":
            Object.HardAttack *= 1.1
        if rule == "Ignore les couverts":
            Object.SoftAttack *= 1.2
        if rule == "Blast 3'":
            Object.SoftAttack *= 1.1
            Object.HardAttack += 1.02
        if rule == "Blast 5'":
            Object.SoftAttack *= 1.2
            Object.HardAttack += 1.05
# Weapons type
    if Object.Type == "Lourde":
        Object.Defense *= 1.2
    if Object.Type == "Assaut":
        Object.Breakthrought *= 1.2
    if Object.Type == "Tir Rapide": pass
    if Object.Type == "Salve":
        Object.Defense *= 1.1
        Object.Breakthrought = 1.1
# Weapon Range
    if Object.Range == (0 or None): pass # melee weapons
    if Object.Range <= 8:
        Object.SoftAttack *= 0.4
        Object.HardAttack *= 0.4
        Object.Defense *= 0.4
        Object.Breakthrought *= 0.4
    elif Object.Range <= 12:
        Object.SoftAttack *= 0.6
        Object.HardAttack *= 0.6
        Object.Defense *= 0.6
        Object.Breakthrought *= 0.6
    elif Object.Range <= 18:
        Object.SoftAttack *= 0.8
        Object.HardAttack *= 0.8
        Object.Defense *= 0.8
        Object.Breakthrought *= 0.8
    elif Object.Range >= 30:
        Object.SoftAttack *= 1.2
        Object.HardAttack *= 1.2
        Object.Defense *= 1.2
        Object.Breakthrought *= 1.2
    elif Object.Range >= 36:
        Object.SoftAttack *= 1.4
        Object.HardAttack *= 1.4
        Object.Defense *= 1.4
        Object.Breakthrought *= 1.4

def setUpgradeBonus(company):
    from W40K.LandBattles.Company import Company
    assert type(company) == Company, "Argument must be a company"
# Coefs des bonus à 1 de base
    SoftAttack_Bonus = 1
    HardAttack_Bonus = 1
    SoftMeleeAttack_Bonus = 1
    HardMeleeAttack_Bonus = 1
    Defense_Bonus = 1
    Breakthrought_Bonus = 1
    for el in company.Upgrade: # Additionne tout les bonus des Upgrades
        equip_ratio = el.Quantity/company.Manpower  # quantité d'upgrade par rapport au Manpower
    # Cette opération est pour incorporer le :equip_ratio: dans les bonus
        SoftAttack_Bonus *= 1 + (el.SoftAttack_Bonus-1)*equip_ratio
        HardAttack_Bonus *= 1 + (el.HardAttack_Bonus-1)*equip_ratio
        SoftMeleeAttack_Bonus *= 1 + (el.SoftMeleeAttack_Bonus-1)*equip_ratio
        HardMeleeAttack_Bonus *= 1 + (el.HardMeleeAttack_Bonus-1)*equip_ratio
        Defense_Bonus *= 1 + (el.Defense_Bonus-1)*equip_ratio
        Breakthrought_Bonus *= 1 + (el.Breakthrought_Bonus-1)*equip_ratio
# Application des bonus
    company.SoftAttack = company.SoftAttack*SoftAttack_Bonus
    company.HardAttack = company.HardAttack*HardAttack_Bonus
    company.SoftMeleeAttack = company.SoftMeleeAttack*SoftMeleeAttack_Bonus
    company.HardMeleeAttack = company.HardMeleeAttack*HardMeleeAttack_Bonus
    company.Defense = company.Defense*Defense_Bonus
    company.Breakthrought = company.Breakthrought*Breakthrought_Bonus

def setUnitBonus(unit):
    #assert type(unit) == Unit
    for rule in unit.SpecialRules:
        if rule == "And they shall know no fear":
            unit.ORG *= 2

def round_Stats(Object):
    Dico = Object.__dict__
    for key in Dico:
        try:    Dico[key] = round(Dico[key],2)
        except: pass

def set_Quantity(Object,Quantity):
    """
    Modifie la quantité de :Unit: et modifie les stats en fonction
    :param Quantity: Nombre de cette unité
    """
    Object.Quantity = Quantity
    Object.HOI4_Profil()

def check_lists(self):
    from W40K.UnitCreator.Class.Weapons import Weapon
    for el in self.Equipement:
        assert type(el) is Weapon , "Each element of Equipement list must be a :Weapon class:"


"""
def saveInCSV(Object):
    Dico1 = Object.__dict__
    Dico2 = getFromDict(Dico1,["HP","ORG",
                               "SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack",
                               "Breaktrhought","Defense","Armor","Piercing","Hardness"
                               ])

    if type(Object) == Infantry: Dict2CSV(Dico2,"Saved_Infantry.csv")
    elif type(Object) == Tank: Dict2CSV(Dico2,"Saved_Tank.csv")
    elif type(Object) == Walker: Dict2CSV(Dico2,"Saved_Walker.csv")
    elif type(Object) == Weapon: Dict2CSV(Dico2,"Saved_Weapon.csv")
    elif type(Object) == Company: Dict2CSV(Dico2,"Saved_Company.csv")
    else: return TypeError , "Object must be Infantry, Walker, Tank, Weapon or Company. Save is not possible"
"""