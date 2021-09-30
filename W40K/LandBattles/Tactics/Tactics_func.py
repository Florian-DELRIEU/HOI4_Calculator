from W40K.LandBattles.Tactics.Tactics_list import Tactic
import random as rd
import numpy as np
from  W40K.LandBattles.Tactics.Tactics_list import ATK_tactics, ATK_HB_tactics, ATK_CQ_tactics, ATK_SB_tactics, ATK_TW_tactics
from  W40K.LandBattles.Tactics.Tactics_list import DEF_tactics, DEF_HB_tactics, DEF_CQ_tactics, DEF_SB_tactics, DEF_TW_tactics


########################################################################################################################

def choose_Tactics(Battle):
    """
    Choisi une tactique selon une sélection pondéré
        - run change-weight
        - run SELF
        - run apply_tactics
        - run set_CAC_limit
    """
    change_weight(Battle)
    #assert type(Battle) is Battle , "Battle must be an :battle: type"
    ATK_tactic_list = list()
    DEF_tactic_list = list()
    if Battle.Phase == "Default":
        ATK_tactic_list = ATK_tactics
        DEF_tactic_list = DEF_tactics
    elif Battle.Phase == "Close Quarter Combat":
        ATK_tactic_list = ATK_CQ_tactics
        DEF_tactic_list = DEF_CQ_tactics
    elif Battle.Phase == "Seize Bridge":
        ATK_tactic_list = ATK_SB_tactics
        DEF_tactic_list = DEF_SB_tactics
    elif Battle.Phase == "Hold Bridge":
        ATK_tactic_list = ATK_HB_tactics
        DEF_tactic_list = DEF_HB_tactics
    elif Battle.Phase == "Tactical Withdraw":
        ATK_tactic_list = ATK_TW_tactics
        DEF_tactic_list = DEF_TW_tactics
    else: return NameError , "Wrong phase name"
    winner = Initiative_round(Battle)
    ATK_Tactic, DEF_Tactic = _choose_tactics(ATK_tactic_list,DEF_tactic_list,winner)
    Battle.ATK_Tactic = ATK_Tactic
    Battle.DEF_Tactic = DEF_Tactic
    isCountered(Battle)
    apply_Tactics(Battle)

def _choose_tactics(ATK_tactic_list,DEF_tactic_list,Initiative_winner):
    ATK_Tactic = Tactic()
    DEF_Tactic = Tactic()
    if Initiative_winner == "ATK":
    # DEF choice
        DEF_tactic_weight = [el.weight for el in DEF_tactic_list]
        DEF_Tactic = rd.choices(DEF_tactic_list, DEF_tactic_weight)[0]
    # Change weight
        try:
            Counter_tactic = [el for el in ATK_tactic_list if el.Name == DEF_Tactic.CounteredBy][0]
            Counter_tactic.weight *= 1.35
        except: pass
    # ATK choice
        ATK_tactic_weight = [el.weight for el in ATK_tactic_list]
        ATK_Tactic = rd.choices(ATK_tactic_list, ATK_tactic_weight)[0]
    if Initiative_winner == "DEF":
    # ATK choice
        ATK_tactic_weight = [el.weight for el in ATK_tactic_list]
        ATK_Tactic = rd.choices(ATK_tactic_list, ATK_tactic_weight)[0]
    # Change weight
        try:
            Counter_tactic = [el for el in DEF_tactic_list if el.Name == ATK_Tactic.CounteredBy][0]
            Counter_tactic.weight *= 1.35
        except: pass
    # DEF choice
        DEF_tactic_weight = [el.weight for el in DEF_tactic_list]
        DEF_Tactic = rd.choices(DEF_tactic_list, DEF_tactic_weight)[0]
    return ATK_Tactic , DEF_Tactic

def isCountered(Battle):
    """
    Chech if a tactic has been countered. Cancel countered ones
    """
    if Battle.DEF_Tactic.Name == Battle.ATK_Tactic.CounteredBy:
        Cancel_Tactic(Battle.ATK_Tactic)
        print("ATK tactic COUNTERED !!")
    if Battle.ATK_Tactic.Name == Battle.DEF_Tactic.CounteredBy:
        Cancel_Tactic(Battle.DEF_Tactic)
        print("DEF tactic COUNTERED !!")

def Cancel_Tactic(Tactic_to_cancel):
    assert type(Tactic_to_cancel) is Tactic
    Tactic_to_cancel.ATK_Damage = 1
    Tactic_to_cancel.ATK_Defense = 1
    Tactic_to_cancel.DEF_Damage = 1
    Tactic_to_cancel.DEF_Defense = 1
    Tactic_to_cancel.CAC = 0
    Tactic_to_cancel.Begin_battle_phase = None


def Initiative_round(Battle):
    ATK_weight = int()
    DEF_weight = int()
    if Battle.ATK_Leader is None:   ATK_weight = 1
    else:   pass  # Need Leader upgrade
    if Battle.DEF_Leader is None:   DEF_weight = 1
    else:   pass  # Need Leader upgrade
    winner = rd.choices(["ATK","DEF"],[ATK_weight,DEF_weight])[0]
    return winner

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
    """Change tactics weight with regards to Generals skills and abilities and terrain"""
    pass