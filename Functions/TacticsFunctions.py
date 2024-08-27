import random as rd
from  Library.TacticList import ATK_TACTICS, ATK_HB_TACTICS, ATK_CQ_TACTICS, ATK_SB_TACTICS, ATK_TW_TACTICS
from  Library.TacticList import DEF_TACTICS, DEF_HB_TACTICS, DEF_CQ_TACTICS, DEF_SB_TACTICS, DEF_TW_TACTICS
from Classes.Tactics import *

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

    # Which tactics lists is used according the battle phase
    if Battle.battle_phase == "Default":
        attacker_tactic_list = ATK_TACTICS
        defender_tactic_list = DEF_TACTICS
    elif Battle.battle_phase == "Close Quarter Combat":
        attacker_tactic_list = ATK_CQ_TACTICS
        defender_tactic_list = DEF_CQ_TACTICS
    elif Battle.battle_phase == "Seize Bridge":
        attacker_tactic_list = ATK_SB_TACTICS
        defender_tactic_list = DEF_SB_TACTICS
    elif Battle.battle_phase == "Hold Bridge":
        attacker_tactic_list = ATK_HB_TACTICS
        defender_tactic_list = DEF_HB_TACTICS
    elif Battle.battle_phase == "Tactical Withdraw":
        attacker_tactic_list = ATK_TW_TACTICS
        defender_tactic_list = DEF_TW_TACTICS
    else: return NameError , "Wrong phase name"

    # Initiative round
    intiative_winner = initiative_round(Battle) # wich side has initiative
    attacker_Tactic, defender_Tactic = _choose_tactic(attacker_tactic_list, defender_tactic_list, intiative_winner) # choose tactics

    # Apply tactic in battle
    Battle.camp_attacker.tactic = attacker_Tactic
    Battle.camp_defender.tactic = defender_Tactic
    if intiative_winner == "DEF" and Battle.camp_defender.tactic.begin_battle_phase is not None:
        Battle.battle_phase = Battle.camp_defender.tactic.begin_battle_phase
    if intiative_winner == "ATK" and Battle.camp_attacker.tactic.begin_battle_phase is not None:
        Battle.battle_phase = Battle.camp_attacker.tactic.begin_battle_phase

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
    if Battle.camp_defender.tactic == Battle.camp_attacker.tactic.countered_by:
        cancel_tactic(Battle.camp_defender.tactic)
        # todo add log print("ATK tactic COUNTERED !!")
    if Battle.camp_attacker.tactic == Battle.camp_defender.tactic.countered_by:
        cancel_tactic(Battle.camp_attacker.tactic)
        # todo add log print("DEF tactic COUNTERED !!")

def cancel_tactic(Tactic_to_cancel):
    """
    Retire tout les bonus d'une tactique
    """
    Tactic_to_cancel.attacker_bonus = 1
    Tactic_to_cancel.defender_bonus = 1
    Tactic_to_cancel.width_bonus = 1
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
    if Battle.camp_attacker.leader is None:   ATK_weight = 1
    else:   pass  # Need Leader upgrade
    if Battle.camp_defender.leader is None:   DEF_weight = 1
    else:   pass  # Need Leader upgrade

    # todo renvoyer directement l'instance des camps
    return rd.choices(["ATK","DEF"],[ATK_weight,DEF_weight])[0]

def apply_tactics(Battle):
    """
    Applique tous les bonus multiplicateurs aux stats de chaque camp en fonctions des tactiques employés
    """
    # Assignations des variables
    DEF_tactic = Battle.camp_defender.tactic
    ATK_tactic = Battle.camp_attacker.tactic

    for division in Battle.camp_defender.frontline:
        #todo augmenter les dégats causé par les attaques
        division.tactic_damage_bonus = DEF_tactic.defender_bonus

    for division in Battle.camp_attacker.frontline:
        division.tactic_damage_bonus = ATK_tactic.attacker_bonus


def change_weight(Battle):
    """
    Change tactics weight with regards to Generals skills and abilities and terrain
    """
    #todo make change_weight functions
    pass