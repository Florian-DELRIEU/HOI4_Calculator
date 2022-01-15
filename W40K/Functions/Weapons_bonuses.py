def apply_SpecialsRules(Weapon):
    """
    Verifie les règles spéciales des :class Weapons: pour ajouté les bonus
    :param Weapon: class weapons
    """
    # Weapons Specials rules
    Rules = Weapon.SpecialsRules
    if "Perforant" in Rules:
        Weapon.SoftAttack *= 1.1
        Weapon.HardAttack *= 1.1
        Weapon.Piercing += 1
    if "Fléau de la chair" in Rules:
        Weapon.SoftAttack *= 1.1
    if "Fléau des chars" in Rules:
        Weapon.HardAttack *= 1.1
    if "Ignore les couverts" in Rules:
        Weapon.SoftAttack *= 1.2
    if "Blast 3'" in Rules:
        Weapon.SoftAttack *= 1.1
        Weapon.HardAttack *= 0.4
    if "Blast 5'" in Rules:
        Weapon.SoftAttack *= 1.2
        Weapon.HardAttack *= 0.6
    if "Krak Grenade" in Rules:
        Weapon.SoftAttack *= 0
    if ("Melta" or "Fusion") in Rules:
        Weapon.HardAttack *= 1.5
    if "Defensive Grenade" in Rules:
        Weapon.Defense_bonus *= 1.15
    if "Assault Grenade" in Rules:
        Weapon.Breakthrought_bonus *= 1.15


########################################################################################################################

def apply_WeaponsType(Weapon):  # sourcery skip: switch

    # Weapons type
    if Weapon.isGrenade(): pass # Pour que les grenades ne soient pas affectés par ces bonus
    elif Weapon.Type == "Lourde":
        Weapon.Defense_bonus *= 1.7
        Weapon.Breakthrought_bonus *= 0.3
    elif Weapon.Type == "Assaut":
        Weapon.Defense_bonus *= 0.5
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
    if Weapon.Range == (0 or None):  # melee weapons
        pass
    elif Weapon.Range <= 8:
        Weapon.SoftAttack *= 0.4
        Weapon.HardAttack *= 0.4
    elif 8 < Weapon.Range <= 18:
        Weapon.SoftAttack *= 0.6
        Weapon.HardAttack *= 0.6
    elif 18 < Weapon.Range <= 24:
        Weapon.SoftAttack *= 0.8
        Weapon.HardAttack *= 0.8
    elif 24 < Weapon.Range <= 30:
        Weapon.SoftAttack *= 1.2
        Weapon.HardAttack *= 1.2
    elif 30 < Weapon.Range <= 36:
        Weapon.SoftAttack *= 1.4
        Weapon.HardAttack *= 1.4
    elif 36 < Weapon.Range <= 42:
        Weapon.SoftAttack *= 1.6
        Weapon.HardAttack *= 1.6
    elif 42 < Weapon.Range <= 48:
        Weapon.SoftAttack *= 1.8
        Weapon.HardAttack *= 1.8
    elif 48 < Weapon.Range <= 72:
        Weapon.SoftAttack *= 2.0
        Weapon.HardAttack *= 2.0
    elif 72 < Weapon.Range <= 96:
        Weapon.SoftAttack *= 2.2
        Weapon.HardAttack *= 2.2
    elif 96 < Weapon.Range <= 120:
        Weapon.SoftAttack *= 2.4
        Weapon.HardAttack *= 2.4
    elif 120 < Weapon.Range <= 240:
        Weapon.SoftAttack *= 3.0
        Weapon.HardAttack *= 3.0
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
    Weapon.Breakthrought_bonus *= 1 #1.1*(Weapon.Cadence - 1)
    Weapon.Defense_bonus *= 1 #.1*(Weapon.Cadence - 1)