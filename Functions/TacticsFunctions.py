import random as rd
from Classes.Tactics import *
from Functions.TacticTriggersFunctions import *

########################################################################################################################


def choose_tactic(Battle):
    from Library.TacticList import ATK_TACTICS, ATK_HB_TACTICS, ATK_CQ_TACTICS, ATK_SB_TACTICS, ATK_TW_TACTICS
    from Library.TacticList import DEF_TACTICS, DEF_HB_TACTICS, DEF_CQ_TACTICS, DEF_SB_TACTICS, DEF_TW_TACTICS
    """
    Choisi une tactique selon une sélection pondérée
        - run "change-weight"
        - run SELF
        - run _choose_tactic
        - run apply_tactics
        - run set_CAC_limit
    """

    # Which tactics lists is used according the battle phase
    if Battle.battle_phase == BattlePhase.DEFAULT:
        attacker_tactic_list = ATK_TACTICS
        defender_tactic_list = DEF_TACTICS
    elif Battle.battle_phase == BattlePhase.CLOSE_QUARTER_COMBAT:
        attacker_tactic_list = ATK_CQ_TACTICS
        defender_tactic_list = DEF_CQ_TACTICS
    elif Battle.battle_phase == BattlePhase.SEIZE_BRIDGE:
        attacker_tactic_list = ATK_SB_TACTICS
        defender_tactic_list = DEF_SB_TACTICS
    elif Battle.battle_phase == BattlePhase.HOLD_BRIDGE:
        attacker_tactic_list = ATK_HB_TACTICS
        defender_tactic_list = DEF_HB_TACTICS
    elif Battle.battle_phase == BattlePhase.TACTICAL_WITHDRAW:
        attacker_tactic_list = ATK_TW_TACTICS
        defender_tactic_list = DEF_TW_TACTICS
    else: return NameError , "Wrong phase name"

    change_weight(Battle,attacker_tactic_list,defender_tactic_list)
    # remove tactics that cannot be choose
    attacker_tactic_list = [tactic for tactic in attacker_tactic_list if tactic.weight * tactic.weight_mult > 0]
    defender_tactic_list = [tactic for tactic in defender_tactic_list if tactic.weight * tactic.weight_mult > 0]


    # Initiative round
    #todo fixme from here
    intiative_winner = initiative_round(Battle) # wich side has initiative
    attacker_Tactic, defender_Tactic = _choose_tactic(attacker_tactic_list, defender_tactic_list, intiative_winner) # choose tactics

    # Apply tactic in battle
    Battle.camp_attacker.tactic = attacker_Tactic
    Battle.camp_defender.tactic = defender_Tactic
    if intiative_winner == "DEF" and Battle.camp_defender.tactic.begin_battle_phase is not None:
        Battle.battle_phase = Battle.camp_attacker.tactic.begin_battle_phase
        Battle.battle_phase = Battle.camp_defender.tactic.begin_battle_phase
    if intiative_winner == "ATK" and Battle.camp_attacker.tactic.begin_battle_phase is not None:
        Battle.battle_phase = Battle.camp_defender.tactic.begin_battle_phase
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
        DEF_Tactic = rd.choices(DEF_tactic_list, [el.weight*el.weight_mult for el in DEF_tactic_list])[0]
        # Change weight for try counter DEF tactic
        try: # Increase weight if counter tactic exist
            Counter_tactic = [el for el in ATK_tactic_list if el.name == DEF_Tactic.countered_by][0]
            Counter_tactic.weight_mult *= 1.35
        except: pass # if counter tactic doesn't exist
        # ATK tactics weighted choice finnaly
        ATK_Tactic = rd.choices(ATK_tactic_list, [el.weight*el.weight_mult for el in ATK_tactic_list] )[0]

    if Initiative_winner == "DEF":
        # ATK choice first
        ATK_Tactic = rd.choices(ATK_tactic_list, [el.weight*el.weight_mult for el in ATK_tactic_list] )[0]
        try: # Change weight for try counter ATK tactic
            Counter_tactic = [el for el in DEF_tactic_list if el.name == ATK_Tactic.countered_by][0]  # Quel est la tactique de contre ?
            Counter_tactic.weight_mult *= 1.35
        except: pass
    # DEF choice
        DEF_Tactic = rd.choices(DEF_tactic_list, [el.weight*el.weight_mult for el in DEF_tactic_list] )[0]
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
        Le round se déroule en plusieurs étapes
        1- On compare la valeur max de reconnaissance parmis les divisions des deux camps. Celui qui à la plus grosse
         valeur gagne 5 niveau.
        2- La compétence des Leaders est ajouté
        3- Le camp avec le niveau de compétence effectif le plus élevé obtient l'initiative, les égalités favorisant
        le défenseur.

        NOTA: Dans cette version les niveau de competences sont des poids permettant un choix pondéré du vainqueur.
    """
    ATK_weight = 1
    DEF_weight = 1
    ATK_max_reco = max(division.recon for division in Battle.camp_attacker.divisions)
    DEF_max_reco = max(division.recon for division in Battle.camp_defender.divisions)

    ATK_weight += Battle.camp_attacker.leader.level
    DEF_weight += Battle.camp_defender.leader.level

    if ATK_max_reco > DEF_max_reco:
        ATK_weight += 5
    elif DEF_max_reco > ATK_max_reco:
        DEF_weight += 5
    else: pass

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


def change_weight(Battle,ATK_tactic,DEF_tactic):
    """
    Change tactics weight with regards to Generals skills and abilities and terrain
    """
    # Variables initialisations
    Attacker = Battle.camp_attacker
    ATK_leader = Battle.camp_attacker.leader
    Defender = Battle.camp_defender
    DEF_leader = Battle.camp_defender.leader

    for tactic in ATK_tactic:
    # Classic Phase
        if tactic.name == "Assault":
            if Battle.terrain.name == "Urban":
                tactic.weight_mult *= 5
            if "Agressive Assaulter" in ATK_leader.traits:
                tactic.weight_mult *= 2

        if tactic.name == "Encirclement":
            if (has_reserves_available(Attacker)
            and has_full_width(Battle,Attacker))\
            and (ATK_leader.level - DEF_leader.level > 0
                or "Panzer Leader" in ATK_leader.traits
                or "Trickster" in ATK_leader.traits):
                tactic.weight_mult = 1
                if ("Panzer Expert" in ATK_leader.traits
                    or "Combined Arms Expert" in ATK_leader.traits):
                    tactic.weight_mult = 2

        if tactic.name == "Shock":
            if "Agressive Assaulter" in ATK_leader.traits:
                tactic.weight_mult = 2

        if tactic.name == "Breakthrough":
            if has_hardness_over(Attacker,50) or ATK_leader.level - DEF_leader.level > 1:
                tactic.weight_mult = 1

        if tactic.name == "Blitz":
            if (has_hardness_over(Battle.camp_attacker,50)
            #todo and not have Soviet focus "Glory of red army"
            and (ATK_leader.level > 2
                 or "Panzer Leader" in ATK_leader.traits
                 or ATK_leader.level - DEF_leader.level > 1)):
                tactic.weight_mult = 1
                if ("Panzer Expert" in ATK_leader.traits
                        or "Combined Arms Expert" in ATK_leader.traits):
                    tactic.weight_mult = 2

        if tactic.name == "Masterful Blitz":
            if (has_hardness_over(Battle.camp_attacker,50)
            and (ATK_leader.level > 2
                 or "Panzer Leader" in ATK_leader.traits
                 or ATK_leader.level - DEF_leader.level > 1)):
                tactic.weight_mult = 1
                if ("Panzer Expert" in ATK_leader.traits
                        or "Combined Arms Expert" in ATK_leader.traits):
                    tactic.weight_mult = 2

        if tactic.name == "Seize Bridge":
            if (has_river(Battle)
            and (ATK_leader.level > 3
                    or ("Offensive Doctrine" in ATK_leader.traits and ATK_leader.level < 2))):
                tactic.weight_mult = 1

        if tactic.name == "Mass Charge":
            if has_reserves_available(Battle.camp_attacker) and has_full_width(Battle, Battle.camp_attacker):
                tactic.weight_mult = 1

        if tactic.name == "Banzai Charge": pass
            #todo if camp si japan

    # Phase Seize Bridge
        if tactic.name == "Defend Bridge":
            if ATK_leader.level > 4:
                tactic.weight_mult = 1

    # Phase Hold Bridge
        if tactic.name == "Rush Bridge":
            if ATK_leader.level > 4:
                tactic.weight_mult = 1


    for tactic in DEF_tactic:

        if tactic.name == "Counter-Attack":
            if DEF_leader.level - ATK_leader.level > 0:
                tactic.weight_mult = 1
                if "Unyielding Defender" in DEF_leader.traits:
                    tactic.weight_mult = 2

        if tactic.name == "Tactic Withdrawal":
            if (DEF_leader.level - ATK_leader.level > 0
            or "Trickster" in DEF_leader.traits):
                tactic.weight_mult = 1

        if tactic.name == "Ambush":
            if (DEF_leader.level - ATK_leader.level > 1
            or DEF_leader.level > 2
            or "Trickster" in DEF_leader.traits):
                tactic.weight_mult = 1

        if tactic.name == "Elastic Defense":
            if (DEF_leader.level > 2
            or "Defensive Doctrine" in DEF_leader.traits):
                tactic.weight_mult = 1

        if tactic.name == "Backhand Blow":
            if (DEF_leader.level > 4
            or ("Trickster" in DEF_leader.traits
                and DEF_leader.level > 3)):
                tactic.weight_mult = 1

        if tactic.name == "Hold Bridge":
            if (has_river(Battle)
            and (DEF_leader.level > 2
                or "Defensive Doctrine" in DEF_leader.traits)):
                tactic.weight_mult = 1

        if tactic.name == "Guerrilla Tactics":
            if (DEF_leader.level > 2
                or "Trickster" in DEF_leader.traits):
                tactic.weight_mult = 1

    # Phase Seize Bridge
        if tactic.name == "Reckless Assault":
            if DEF_leader.level < 3:
                tactic.weight_mult = 1

        if tactic.name == "Recapture Bridge":
            if DEF_leader.level > 2 or "Trickster" in DEF_leader.traits:
                tactic.weight_mult = 1

    # Phase Hold Bridge
        if tactic.name == "Holding Bridge":
            if DEF_leader.level < 3:
                tactic.weight_mult = 1

        if tactic.name == "Defend Bridge":
            if DEF_leader.level > 2 or "Trickster" in DEF_leader.traits:
                tactic.weight_mult = 1

        pass