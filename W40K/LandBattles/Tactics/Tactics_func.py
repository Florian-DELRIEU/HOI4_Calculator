from W40K.LandBattles.Tactics.Tactics_list import Tactic
import W40K.LandBattles.Tactics.Tactics_list as tac
import random as rd
import numpy as np


# Extrait les tactics de :Tactic_list: DEF et ATK séparés
DICO = tac.__dict__
LIST_atk = list()
LIST_def = list()
for key in DICO.keys():
    if type(DICO[key]) in [Tactic]:
        if not DICO[key].isDefenseTactic:
            LIST_atk.append(DICO[key]) # List d'Attaquand
        elif DICO[key].isDefenseTactic:
            LIST_def.append(DICO[key]) # List de Defenseur

########################################################################################################################

def choose_Tactics(Battle):
    change_weight(Battle)
    #assert type(Battle) is Battle , "Battle must be an :battle: type"
    ATK_tactic_weight = [el.weight for el in LIST_atk]
    DEF_tactic_weight = [el.weight for el in LIST_def]
    Battle.ATK_Tactic = rd.choices(LIST_atk,ATK_tactic_weight)
    Battle.DEF_Tactic = rd.choices(LIST_def,DEF_tactic_weight)
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
    if Battle.CAC_level > 0.3:
        tac.CloseQuarterAttack.weight = 1