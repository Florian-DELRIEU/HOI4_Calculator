import random as rd
from  Lib.TacticsList import ATK_TACTICS, ATK_HB_TACTICS, ATK_CQ_TACTICS, ATK_SB_TACTICS, ATK_TW_TACTICS
from  Lib.TacticsList import DEF_TACTICS, DEF_HB_TACTICS, DEF_CQ_TACTICS, DEF_SB_TACTICS, DEF_TW_TACTICS
from Class.Tactics import *

########################################################################################################################

def choose_tactic(Battle):
    """
    Choisi une tactique selon une sélection pondérée
        - run "change-weight"
        - run SELF
        - run _choose_tactic
        - run apply_tactics
        - run set_CAC_limit
    """
    change_weight(Battle)

    # Which tactics lists is used according the battle phase
    if Battle.Phase == "Default":
        attacker_tactic_list = ATK_TACTICS
        defender_tactic_list = DEF_TACTICS
    elif Battle.Phase == "Close Quarter Combat":
        attacker_tactic_list = ATK_CQ_TACTICS
        defender_tactic_list = DEF_CQ_TACTICS
    elif Battle.Phase == "Seize Bridge":
        attacker_tactic_list = ATK_SB_TACTICS
        defender_tactic_list = DEF_SB_TACTICS
    elif Battle.Phase == "Hold Bridge":
        attacker_tactic_list = ATK_HB_TACTICS
        defender_tactic_list = DEF_HB_TACTICS
    elif Battle.Phase == "Tactical Withdraw":
        attacker_tactic_list = ATK_TW_TACTICS
        defender_tactic_list = DEF_TW_TACTICS
    else: return NameError , "Wrong phase name"

    # Initiative round
    intiative_winner = initiative_round(Battle) # wich side has initiative
    attacker_Tactic, defender_Tactic = _choose_tactic(attacker_tactic_list, defender_tactic_list, intiative_winner) # choose tactics

    # Apply tactic in battle
    Battle.attacker_tactic = attacker_Tactic
    Battle.defender_tactic = defender_Tactic

    is_countered(Battle) # test if any tactics has been coutered
    apply_tactics(Battle) # apply bonuses

def _choose_tactic(ATK_tactic_list, DEF_tactic_list, Initiative_winner):
    """
    Le perdant du :initiative round: choisi la tactique en premier. Ensuite le gagnant tente de le contrer.
    :return: Tactiques choisis par les deux camps
    """
    ATK_Tactic = Tactic()
    DEF_Tactic = Tactic()
    if Initiative_winner == "ATK":
        # DEF tactics weighted choice first
        DEF_Tactic = rd.choices(DEF_tactic_list, [el.weight for el in DEF_tactic_list])[0]
        # Change weight for try counter DEF tactic
        try: # Increase weight if counter tactic exist
            Counter_tactic = [el for el in ATK_tactic_list if el.name == DEF_Tactic.countered_by][0]
            Counter_tactic.weight *= 1.35
        except: pass # if counter tactic doesn't exist
        # ATK tactics weighted choice finnaly
        ATK_Tactic = rd.choices(ATK_tactic_list, [el.weight for el in ATK_tactic_list] )[0]

    if Initiative_winner == "DEF":
        # ATK choice first
        ATK_Tactic = rd.choices(ATK_tactic_list, [el.weight for el in ATK_tactic_list] )[0]
        try: # Change weight for try counter ATK tactic
            Counter_tactic = [el for el in DEF_tactic_list if el.name == ATK_Tactic.countered_by][0]  # Quel est la tactique de contre ?
            Counter_tactic.weight *= 1.35
        except: pass
    # DEF choice
        DEF_Tactic = rd.choices(DEF_tactic_list, [el.weight for el in DEF_tactic_list] )[0]
    return ATK_Tactic , DEF_Tactic

def is_countered(Battle):
    """
    Check if a tactic has been countered. Cancel countered ones
    """
    if Battle.defender_tactic.name == Battle.attacker_tactic.countered_by:
        cancel_tactic(Battle.attacker_tactic)
        print("ATK tactic COUNTERED !!")
    if Battle.attacker_tactic.name == Battle.defender_tactic.countered_by:
        cancel_tactic(Battle.defender_tactic)
        print("DEF tactic COUNTERED !!")

def cancel_tactic(Tactic_to_cancel):
    """
    Retire tout les bonus d'une tactique
    """
    assert type(Tactic_to_cancel) is Tactic
    Tactic_to_cancel.attacker_damage = 1
    Tactic_to_cancel.attacker_defense = 1
    Tactic_to_cancel.defender_damage = 1
    Tactic_to_cancel.defender_defense = 1
    Tactic_to_cancel.CAC = 0
    Tactic_to_cancel.begin_battle_phase = None

def initiative_round(Battle):
    # sourcery skip: assign-if-exp, remove-redundant-pass
    """
    Choisis quel camp aura l'initiative
        - Le camps qui remporte l'initiative choisiras sa tacttique en second pour essayer de contrer l'autre camps.
        - Basic pour le moment car leaders ne sont pas ajoutés
    """
    ATK_weight = int()
    DEF_weight = int()
    if Battle.AttackerLeader is None:   ATK_weight = 1
    else:   pass  # Need Leader upgrade
    if Battle.DefenderLeader is None:   DEF_weight = 1
    else:   pass  # Need Leader upgrade

    return rd.choices(["ATK","DEF"],[ATK_weight,DEF_weight])[0]

def apply_tactics(Battle):
    """
    Applique tout les bonus multiplicateurs aux stats de chaque camps en fonctions des tactiques employés
    """
    # Assignations des variables
    DEF = Battle.defender
    DEF_tactic = Battle.defender_tactic
    ATK = Battle.attacker
    ATK_tactic = Battle.attacker_tactic

    # Bonus for defender side
    DEF.sa = DEF.sa*DEF_tactic.defender_damage*ATK_tactic.defender_damage
    DEF.ha = DEF.ha*DEF_tactic.defender_damage*ATK_tactic.defender_damage
    DEF.defense = DEF.defense*DEF_tactic.defender_defense*ATK_tactic.defender_defense

    # Bonus for attacker side
    ATK.sa = ATK.sa*ATK_tactic.attacker_damage*ATK_tactic.attacker_damage
    ATK.ha = ATK.ha*ATK_tactic.attacker_damage*ATK_tactic.attacker_damage
    ATK.defense = ATK.defense*ATK_tactic.attacker_defense*ATK_tactic.attacker_defense

def change_weight(Battle):
    """Change tactics weight with regards to Generals skills and abilities and terrain"""
    pass