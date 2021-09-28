from W40K.LandBattles.Tactics.Tactics_list import Tactic
import random as rd
import numpy as np
from  W40K.LandBattles.Tactics.Tactics_list import ATK_list, ATK_HB_list, ATK_CQ_list, ATK_SB_list, ATK_TW_list
from  W40K.LandBattles.Tactics.Tactics_list import DEF_list, DEF_HB_list, DEF_CQ_list, DEF_SB_list, DEF_TW_list


########################################################################################################################

def choose_Tactics(Battle):
    """
    Choisi une tactique selon une sélection pondéré
        - run apply_tactics
        - run set_CAC_limit
    """
    change_weight(Battle)
    #assert type(Battle) is Battle , "Battle must be an :battle: type"
    ATK_tactic_weight = [el.weight for el in ATK_list]
    DEF_tactic_weight = [el.weight for el in DEF_list]
    Battle.ATK_Tactic = rd.choices(ATK_list,ATK_tactic_weight)
    Battle.DEF_Tactic = rd.choices(DEF_list,DEF_tactic_weight)
    apply_Tactics(Battle)

def apply_Tactics(Battle):
    DEF = Battle.DEF
    DEF_Tac = Battle.DEF_Tactic
    ATK = Battle.ATK
    ATK_Tac = Battle.ATK_Tactic
# Bonus for DEF
    DEF.SoftAttack = DEF.SoftAttack * DEF_Tac.DEF_Damage * ATK_Tac.DEF_Damage
    DEF.HardAttack = DEF.HardAttack * DEF_Tac.DEF_Damage * ATK_Tac.DEF_Damage
    DEF.Defense = DEF.Defense * DEF_Tac.DEF_Defense * ATK_Tac.DEF_Defense
# Bonus for ATK
    ATK.SoftAttack = ATK.SoftAttack * ATK_Tac.ATK_Damage * ATK_Tac.ATK_Damage
    ATK.HardAttack = ATK.HardAttack * ATK_Tac.ATK_Damage * ATK_Tac.ATK_Damage
    ATK.Defense = ATK.Defense * ATK_Tac.ATK_Defense * ATK_Tac.ATK_Defense
# Cac limit
    set_CAC_limit(Battle)

def set_CAC_limit(Battle):
    DEF_Tac = Battle.DEF_Tactic
    ATK_Tac = Battle.ATK_Tactic
    Battle.CAC_limit = Battle.CAC_limit + np.sum(DEF_Tac.CAC + ATK_Tac.CAC)
    if Battle.CAC_limit < -0.5: Battle.CAC_limit = -.5
    elif Battle.CAC_limit > 1.5: Battle.CAC_limit = 1.5

def update_CAC(Battle):
    CAC_current = Battle.CAC_level
    CAC_limit = Battle.CAC_limit
    CAC_drift = (CAC_limit - CAC_current) / 10
    Battle.CAC_level = CAC_current + CAC_drift
    if Battle.CAC_level < 0: Battle.CAC_level = 0
    elif Battle.CAC_level > 1: Battle.CAC_level = 1

def change_weight(Battle):
    DEF_Tac = Battle.DEF_Tactic
    ATK_Tac = Battle.ATK_Tactic