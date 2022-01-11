from W40K.Lists.Tactics_list import Tactic
import random as rd
import numpy as np
from MyPack.Utilities import truncDecimal
from  W40K.Lists.Tactics_list import ATK_tactics, ATK_HB_tactics, ATK_CQ_tactics, ATK_SB_tactics, ATK_TW_tactics
from  W40K.Lists.Tactics_list import DEF_tactics, DEF_HB_tactics, DEF_CQ_tactics, DEF_SB_tactics, DEF_TW_tactics

all_Tactics_list = ATK_tactics + ATK_HB_tactics + ATK_CQ_tactics + ATK_SB_tactics + ATK_TW_tactics\
                 + DEF_tactics + DEF_HB_tactics + DEF_CQ_tactics + DEF_SB_tactics + DEF_TW_tactics
########################################################################################################################

def choose_Tactics(Battle):
    """
    Choisi une tactique selon une sélection pondéré
        - run change-weight
        - run SELF
        - run _choose_tactic
        - run apply_tactics
        - run set_CAC_limit
    """
    change_weight(Battle)
# Which tactics lists is used according the battle phase
    if Battle.Current_Phase == "Default":
        ATK_tactic_list = ATK_tactics
        DEF_tactic_list = DEF_tactics
        Battle.Current_Phase == "Default"
    elif Battle.Current_Phase == "Close Quarter Combat":
        ATK_tactic_list = ATK_CQ_tactics
        DEF_tactic_list = DEF_CQ_tactics
    elif Battle.Current_Phase == "Seize Bridge":
        ATK_tactic_list = ATK_SB_tactics
        DEF_tactic_list = DEF_SB_tactics
    elif Battle.Current_Phase == "Hold Bridge":
        ATK_tactic_list = ATK_HB_tactics
        DEF_tactic_list = DEF_HB_tactics
    elif Battle.Current_Phase == "Tactical Withdraw":
        ATK_tactic_list = ATK_TW_tactics
        DEF_tactic_list = DEF_TW_tactics
    else: return NameError , "Wrong phase name"
    winner = Initiative_round(Battle) # wich side has initiative
    ATK_Tactic, DEF_Tactic = _choose_tactics(ATK_tactic_list,DEF_tactic_list,winner) # choose tactics
    Battle.ATK_Tactic = ATK_Tactic
    Battle.DEF_Tactic = DEF_Tactic
    Battle.Initiative_winner = winner
    isCountered(Battle) # test if any tactics has been coutered
    apply_Tactics(Battle) # apply bonuses
    change_BattlePhase(Battle)

def _choose_tactics(ATK_tactic_list,DEF_tactic_list,Initiative_winner):
    """
    Le perdant du :initiative round: choisi la tactique en premier. Ensuite le gagnant tente de le contrer.
    :return: Tactiques choisis par les deux camps
    FIXME
        - Fusionner les boucles pour les cas ou le gagnant est soit le DEF / ATK dans une seule boucle
    """
    ATK_Tactic = Tactic()
    DEF_Tactic = Tactic()
    if Initiative_winner == "ATK":
    # DEF choice first
        DEF_tactic_weight = [el.weight for el in DEF_tactic_list]
        DEF_Tactic = rd.choices(DEF_tactic_list, DEF_tactic_weight)[0]
    # Change weight for try counter DEF tactic
        try: # Increase weight if counter tactic exist
            Counter_tactic = [el for el in ATK_tactic_list if el.Name == DEF_Tactic.CounteredBy][0]
            Counter_tactic.weight *= 1.35
        except: pass # if counter tactic doesn't exist
    # ATK choice finnaly
        ATK_tactic_weight = [el.weight for el in ATK_tactic_list]
        ATK_Tactic = rd.choices(ATK_tactic_list, ATK_tactic_weight)[0]
    if Initiative_winner == "DEF":
    # ATK choice first
        ATK_tactic_weight = [el.weight for el in ATK_tactic_list]
        ATK_Tactic = rd.choices(ATK_tactic_list, ATK_tactic_weight)[0]
        try: # Change weight for try counter ATK tactic
            Counter_tactic = [el for el in DEF_tactic_list if el.Name == ATK_Tactic.CounteredBy][0]
            Counter_tactic.weight *= 1.35
        except: pass
    # DEF choice
        DEF_tactic_weight = [el.weight for el in DEF_tactic_list]
        DEF_Tactic = rd.choices(DEF_tactic_list, DEF_tactic_weight)[0]
    return ATK_Tactic , DEF_Tactic

def isCountered(Battle):
    """
    Check if a tactic has been countered. Cancel countered ones
    """
    if Battle.DEF_Tactic.Name == Battle.ATK_Tactic.CounteredBy:
        Cancel_Tactic(Battle.ATK_Tactic)
        print("ATK tactic COUNTERED !!")
    if Battle.ATK_Tactic.Name == Battle.DEF_Tactic.CounteredBy:
        Cancel_Tactic(Battle.DEF_Tactic)
        print("DEF tactic COUNTERED !!")

def Cancel_Tactic(Tactic_to_cancel):
    """
    Retire tout les bonus d'une tactique
    """
    assert type(Tactic_to_cancel) is Tactic
    Tactic_to_cancel.ATK_Damage = 1
    Tactic_to_cancel.ATK_Defense = 1
    Tactic_to_cancel.DEF_Damage = 1
    Tactic_to_cancel.DEF_Defense = 1
    Tactic_to_cancel.CAC = 0
    Tactic_to_cancel.Begin_battle_phase = None

def Initiative_round(Battle):
    # sourcery skip: assign-if-exp, remove-redundant-pass
    """
    Choisis quel camp aura l'initiative
        - Pas en accord avec le wiki (a voir)
        - Code perso
    """
    DEF_leader = Battle.DEF["Leader"]
    DEF_weight = DEF_leader.Defense_skill + DEF_leader.Level
    ATK_leader = Battle.ATK["Leader"]
    ATK_weight = ATK_leader.Attack_skill + ATK_leader.Level
    return rd.choices(["ATK","DEF"],[ATK_weight,DEF_weight])[0]

def apply_Tactics(Battle):
    DEF = Battle.DEF["Regiment"]
    DEF_Tac = Battle.DEF_Tactic
    ATK = Battle.ATK["Regiment"]
    ATK_Tac = Battle.ATK_Tactic
# Bonus for DEF
    DEF.SoftAttack *= DEF_Tac.DEF_Damage * ATK_Tac.DEF_Damage
    DEF.HardAttack *= DEF_Tac.DEF_Damage * ATK_Tac.DEF_Damage
    DEF.Defense *= DEF_Tac.DEF_Defense * ATK_Tac.DEF_Defense
# Bonus for ATK
    ATK.SoftAttack *= DEF_Tac.ATK_Damage * ATK_Tac.ATK_Damage
    ATK.HardAttack *= DEF_Tac.ATK_Damage * ATK_Tac.ATK_Damage
    ATK.Defense *= DEF_Tac.ATK_Defense * ATK_Tac.ATK_Defense
# Cac limit
    set_CAC_limit(Battle)

def set_CAC_limit(Battle):
    DEF_Tac = Battle.DEF_Tactic
    ATK_Tac = Battle.ATK_Tactic
    if Battle.CAC_limit < 0:    Battle.CAC_limit = 0 # Mets le CAC limit entre 0 et 1
    elif Battle.CAC_limit > 1:  Battle.CAC_limit = 1 # Pour préparer le nouvel CAC limit
    Battle.CAC_limit = Battle.CAC_limit + np.sum(DEF_Tac.CAC + ATK_Tac.CAC)
    if Battle.CAC_limit < -0.5: Battle.CAC_limit = -.5
    elif Battle.CAC_limit > 1.5: Battle.CAC_limit = 1.5

def update_CAC(Battle):
    CAC_current = Battle.CAC_level
    CAC_limit = Battle.CAC_limit
    CAC_drift = (CAC_limit - CAC_current) / 10
    Battle.CAC_level += CAC_drift
    if Battle.CAC_level < 0: Battle.CAC_level = 0
    elif Battle.CAC_level > 1: Battle.CAC_level = 1

def change_BattlePhase(Battle):
    if Battle.Initiative_winner == "ATK":   winner_tactic = Battle.ATK_Tactic
    elif Battle.Initiative_winner == "DEF": winner_tactic = Battle.DEF_Tactic
    else: return AttributeError , "Winner not exists"
    if winner_tactic.Begin_battle_phase != None:
        Battle.Following_Phase = winner_tactic.Begin_battle_phase

def change_weight(Battle):
    """Change tactics weight with regards to Generals skills and abilities and terrain"""
    pass