
def set_LeaderSkills(Battle):
    for side in [Battle.ATK, Battle.DEF]:
        side["Regiment"].__SoftAttack       *= 1.05**side["Leader"].Leader.Attack_skill
        side["Regiment"].__HardAttack       *= 1.05**side["Leader"].Leader.Attack_skill
        side["Regiment"].__SoftMeleeAttack  *= 1.05**side["Leader"].Leader.Attack_skill
        side["Regiment"].__HardMeleeAttack  *= 1.05**side["Leader"].Leader.Attack_skill
        side["Regiment"].__Defense          *= 1.05**side["Leader"].Leader.Defense_skill
        side["Regiment"].__Breakthrought    *= 1.05**side["Leader"].Leader.Defense_skill

def apply_LeaderTactic(Battle):
    """
    Modifie les tactiques en fonctions des Leaders
    """
    for side in [Battle.ATK, Battle.DEF]: # Augmente le poids des tactiques préférés pour chaques camps
        for each_tactic in side["Tactics"]:
            if each_tactic in side["Leader"].Prefered_Tactics:
                each_tactic.weight *= 1.35

def apply_LeaderTraits(Leader):  # sourcery skip: for-index-underscore
    for trait in Leader.Traits_list: pass