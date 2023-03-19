
def set_LeaderSkills(Battle):
    for side in [Battle.ATK, Battle.DEF]:
        side["Regiment"]._Regiment__SoftAttack       *= 1.05**(side["Leader"].Attack_skill-1)
        side["Regiment"]._Regiment__HardAttack       *= 1.05**(side["Leader"].Attack_skill-1)
        side["Regiment"]._Regiment__SoftMeleeAttack  *= 1.05**(side["Leader"].Attack_skill-1)
        side["Regiment"]._Regiment__HardMeleeAttack  *= 1.05**(side["Leader"].Attack_skill-1)
        side["Regiment"]._Regiment__Defense          *= 1.05**(side["Leader"].Defense_skill-1)
        side["Regiment"]._Regiment__Breakthrought    *= 1.05**(side["Leader"].Defense_skill-1)

def apply_LeaderTactic(Battle):
    """
    Modifie les tactiques en fonctions des Leaders
    """
    for side in [Battle.ATK, Battle.DEF]: # Augmente le poids des tactiques préférés pour chaques camps
        for each_tactic in side["Tactics"]:
            if each_tactic.Name in side["Leader"].Prefered_Tactics:
                each_tactic.weight *= 1.35

def apply_LeaderTraits(Leader):  # sourcery skip: for-index-underscore
    pass