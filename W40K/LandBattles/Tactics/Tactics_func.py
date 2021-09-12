from W40K.LandBattles.Tactics.Tactics_list import Tactic
import W40K.LandBattles.Tactics.Tactics_list as Tactics
import random as rd
import numpy as np


# Extrait les tactics de :Tactic_list: DEF et ATK séparés
DICO = Tactics.__dict__
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
    #assert type(Battle) is Battle , "Battle must be an :battle: type"
    Battle.ATK_Tactic = rd.choice(LIST_atk)
    Battle.DEF_Tactic = rd.choice(LIST_def)
    apply_Tactics(Battle)

def apply_Tactics(Battle):
    DEF = Battle.DEF
    DEF_Tac = Battle.DEF_Tactic
# Bonus for DEF
    DEF.SoftAttack *= DEF_Tac.Bonus_SA
    DEF.HardAttack *= DEF_Tac.Bonus_HA
    DEF.SoftMeleeAttack *= DEF_Tac.Bonus_SMA
    DEF.HardMeleeAttack *= DEF_Tac.Bonus_HMA
    DEF.Breakthrought *= DEF_Tac.Bonus_BRK
    DEF.Defense *= DEF_Tac.Bonus_DEF
######################################
    ATK = Battle.ATK
    ATK_Tac = Battle.ATK_Tactic
# Bonus for ATK
    ATK.SoftAttack *= ATK_Tac.Bonus_SA
    ATK.HardAttack *= ATK_Tac.Bonus_HA
    ATK.SoftMeleeAttack *= ATK_Tac.Bonus_SMA
    ATK.HardMeleeAttack *= ATK_Tac.Bonus_HMA
    ATK.Breakthrought *= ATK_Tac.Bonus_BRK
    ATK.Defense *= ATK_Tac.Bonus_DEF
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
