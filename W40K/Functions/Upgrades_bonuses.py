def setUpgradeBonus(company):
    from W40K.Class.Company import Company
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
    company.SoftAttack *= SoftAttack_Bonus
    company.HardAttack *= HardAttack_Bonus
    company.SoftMeleeAttack *= SoftMeleeAttack_Bonus
    company.HardMeleeAttack *= HardMeleeAttack_Bonus
    company.Defense *= Defense_Bonus
    company.Breakthrought *= Breakthrought_Bonus