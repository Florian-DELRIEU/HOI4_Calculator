def setWeapons_SAHA_bonus(Object):
    """
    Verifie les règles spéciales des :class Weapons: pour ajouté les bonus
    :param Object: class weapons
    """
    #assert type(Object) == Weapon , "Object must be :class Weapon:"
# Weapons Specials rules
    Rules = Object.SpecialsRules
    if "Perforant" in Object.SpecialsRules:
        Object.SoftAttack *= 1.1
        Object.HardAttack *= 1.1
        Object.Piercing += 1
    if "Fléau de la chair" in Object.SpecialsRules:
        Object.SoftAttack *= 1.1
    if "Fléau des chars" in Object.SpecialsRules:
        Object.HardAttack *= 1.1
    if "Ignore les couverts" in Object.SpecialsRules:
        Object.SoftAttack *= 1.2
    if "Blast 3'" in Object.SpecialsRules:
        Object.SoftAttack *= 1.1
        Object.HardAttack *= 0.4
    if "Blast 5'" in Object.SpecialsRules:
        Object.SoftAttack *= 1.2
        Object.HardAttack *= 0.6
    if "Krak Grenade" in Object.SpecialsRules:
        Object.SoftAttack *= 0
    if "Fusion" in Object.SpecialsRules:
        Object.HardAttack *= 1.5
# Weapons type
    if Object.Type == "Lourde":     pass
    if Object.Type == "Assaut":     pass
    if Object.Type == "Tir rapide": pass
    if Object.Type == "Salve":      pass
    if Object.Type == "Ordnance":
        Object.SoftAttack *= 1.5
# Weapon Range
    if Object.Range == (0 or None): # melee weapons
        pass
    elif Object.Range <= 8:
        Object.SoftAttack *= 0.4
        Object.HardAttack *= 0.4
    elif 8 < Object.Range <= 18:
        Object.SoftAttack *= 0.6
        Object.HardAttack *= 0.6
    elif 18 < Object.Range <= 24:
        Object.SoftAttack *= 0.8
        Object.HardAttack *= 0.8
    elif 24 < Object.Range <= 30:
        Object.SoftAttack *= 1.2
        Object.HardAttack *= 1.2
    elif 30 < Object.Range <= 36:
        Object.SoftAttack *= 1.4
        Object.HardAttack *= 1.4
    elif 36 < Object.Range <= 48:
        Object.SoftAttack *= 1.6
        Object.HardAttack *= 1.6
    elif 36 < Object.Range <= 48:
        Object.SoftAttack *= 1.8
        Object.HardAttack *= 1.8
    elif 48 < Object.Range <= 72:
        Object.SoftAttack *= 2.0
        Object.HardAttack *= 2.0
    elif 72 < Object.Range <= 96:
        Object.SoftAttack *= 2.2
        Object.HardAttack *= 2.2
    elif 96 < Object.Range <= 120:
        Object.SoftAttack *= 2.4
        Object.HardAttack *= 2.4
    elif 120 < Object.Range <= 240:
        Object.SoftAttack *= 3.0
        Object.HardAttack *= 3.0

########################################################################################################################

def change_weapons_DEFBRK(Weapon):  # sourcery skip: switch
    # Weapons type
    if Weapon.Type == "Lourde":
        Weapon.Defense_bonus *= 1.5
        Weapon.Defense_bonus *= 0
    elif Weapon.Type == "Assaut":
        Weapon.Defense_bonus *= 0.3
        Weapon.Breakthrought_bonus *= 1.5
    elif Weapon.Type == "Tir rapide":
        pass
    elif Weapon.Type == "Salve":
        Weapon.Breakthrought_bonus *= 1.2
        Weapon.Defense_bonus *= 0.8
    elif Weapon.Type == "Ordnance":
        Weapon.Breakthrought_bonus *= 1
        Weapon.Defense_bonus *= 1
    # Weapon Range #Commented
    """
    if Weapon.Range == (0 or None):  # melee weapons
        Weapon.Defense *= 0.3
        Weapon.Breakthrought *= 0.6
    elif Weapon.Range <= 8:
        Weapon.Defense *= 0.6
        Weapon.Breakthrought *= 0.8
    elif 8 < Weapon.Range <= 18:
        Weapon.Defense *= 0.8
        Weapon.Breakthrought *= 0.9
    elif 18 < Weapon.Range <= 24:
        Weapon.Defense *= 1
        Weapon.Breakthrought *= 1
    elif 24 < Weapon.Range <= 30:
        Weapon.Defense *= 1.2
        Weapon.Breakthrought *= 1.1
    elif 30 < Weapon.Range <= 36:
        Weapon.Defense *= 1.4
        Weapon.Breakthrought *= 1.2
    elif 36 < Weapon.Range <= 48:
        Weapon.Defense *= 1.6
        Weapon.Breakthrought *= 1.3
    elif 48 < Weapon.Range <= 72:
        Weapon.Defense *= 1.8
        Weapon.Breakthrought *= 1.4
    elif 72 < Weapon.Range <= 96:
        Weapon.Defense *= 1.8
        Weapon.Breakthrought *= 1.4
    elif 96 < Weapon.Range <= 120:
        Weapon.Defense *= 2.0
        Weapon.Breakthrought *= 1.5
    elif 120 < Weapon.Range <= 240:
        Weapon.Defense *= 2.5
        Weapon.Breakthrought *= 1.8
    """
    # Weapons Fire rate
    Weapon.Breakthrought_bonus *= 1.1*(Weapon.Cadence - 1)
    Weapon.Defense_bonus *= 1.1*(Weapon.Cadence - 1)