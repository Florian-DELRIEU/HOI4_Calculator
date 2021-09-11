from MyPack.Convert import Dict2CSV
import W40K.UnitCreator.Unit_list as main
from W40K.UnitCreator.Class.Unit import Infantry,Tank,Walker
from W40K.UnitCreator.Class.Weapons import Weapon


DICO_1 = main.__dict__    # toutes les variables et classes de main dans un dico
DICO_2A = dict()           # Pour les sauvegardes
DICO_2B = dict()           # Pour les sauvegardes
DICO_3A = dict()
DICO_3B = dict()

# For UNITS
for key in DICO_1.keys():
    if type(DICO_1[key]) in [Infantry, Tank, Walker]:
        DICO_2A[key] = DICO_1[key]
# For WEAPONS
for key in DICO_1.keys():
    if type(DICO_1[key]) in [Weapon]:
        DICO_2B[key] = DICO_1[key]
del DICO_1

# Saves UNITS
fisrt_column_A = ["HP","ORG","SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack","Defense",
            "Breakthrought","Armor","Piercing","Hardness"]
DICO_3A["Units"] = fisrt_column_A
for key in DICO_2A.keys():
    cur = DICO_2A[key]
    assert type(cur) == Infantry or Tank or Walker
    cur_list = [cur.HP,cur.ORG,cur.SoftAttack,cur.HardAttack,cur.SoftMeleeAttack,cur.HardMeleeAttack,cur.Defense,
            cur.Breakthrought,cur.Armor,cur.Piercing,cur.Hardness]
    DICO_3A[key] = cur_list

# Saves WEAPONS
fisrt_column_B = ["SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack","Defense",
            "Breakthrought"]
DICO_3B["Weapons"] = fisrt_column_B
for key in DICO_2B.keys():
    cur = DICO_2B[key]
    assert type(cur) == Weapon
    cur_list = [cur.SoftAttack,cur.HardAttack,cur.SoftMeleeAttack,cur.HardMeleeAttack,cur.Defense,
            cur.Breakthrought]
    DICO_3B[key] = cur_list

Dict2CSV(DICO_3A, "SaveUnit.csv")
Dict2CSV(DICO_3B, "SaveWeapons.csv")