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
            Object.HardAttack *= 1.02
        if rule == "Blast 5'":
            Object.SoftAttack *= 1.2
            Object.HardAttack *= 1.05
        if rule == "Krak Grenade":
            Object.SoftAttack *= 0
        if rule == "Fusion":
            Object.HardAttack *= 1.5

# Weapons type
    if Object.Type == "Lourde":
        Object.Defense *= 10
    if Object.Type == "Assaut":
        Object.Breakthrought *= 10
    if Object.Type == "Tir rapide":
        Object.Breakthrought *= 2
        Object.Defense *= 8
    if Object.Type == "Salve":
        Object.Breakthrought = 4
        Object.Defense *= 6
    if Object.Type == "Ordnance":
        Object.SoftAttack *= 1.5
        Object.Breakthrought = 4
        Object.Defense *= 6

# Weapon Range
    if Object.Range == (0 or None): # melee weapons
        Object.Defense *= 0.3
        Object.Breakthrought *= 0.6
    elif Object.Range <= 8:
        Object.SoftAttack *= 0.4
        Object.HardAttack *= 0.4
        Object.Defense *= 0.6
        Object.Breakthrought *= 0.8
    elif 8 < Object.Range <= 18:
        Object.SoftAttack *= 0.6
        Object.HardAttack *= 0.6
        Object.Defense *= 0.8
        Object.Breakthrought *= 0.9
    elif 18 < Object.Range <= 24:
        Object.SoftAttack *= 0.8
        Object.HardAttack *= 0.8
        Object.Defense *= 1
        Object.Breakthrought *= 1
    elif 24 < Object.Range <= 30:
        Object.SoftAttack *= 1.2
        Object.HardAttack *= 1.2
        Object.Defense *= 1.2
        Object.Breakthrought *= 1.1
    elif 30 < Object.Range <= 36:
        Object.SoftAttack *= 1.4
        Object.HardAttack *= 1.4
        Object.Defense *= 1.4
        Object.Breakthrought *= 1.2
    elif 36 < Object.Range <= 48:
        Object.SoftAttack *= 1.4
        Object.HardAttack *= 1.4
        Object.Defense *= 1.6
        Object.Breakthrought *= 1.3