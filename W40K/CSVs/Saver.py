"""
Extraits les :class Unit et Weapons: depuis le fichier :Unit_list: pour sauvegarder leurs profil HOI IV dans deux fichiers CSV distincs 
"""
from MyPack.Convert import Dict2CSV
import W40K.Lists.Companies_list as CompanyList
import W40K.Lists.Unit_list as UnitsWeapons_List
from W40K.Class.Unit import Infantry,Tank,Walker
from W40K.Class.Weapons import Weapon
from W40K.Class.Company import Company
from W40K.Functions.Functions import round_Stats


DICO_1A = UnitsWeapons_List.__dict__    # toutes les variables et classes de main dans un dico
DICO_1B = CompanyList.__dict__    # toutes les variables et classes de main dans un dico
DICO_2A = dict()           # Units
DICO_2B = dict()           # Weapons
DICO_2C = dict()           # Companies
DICO_3A = dict()
DICO_3B = dict()
DICO_3C = dict()

# For UNITS
for key in DICO_1A.keys():
    if type(DICO_1A[key]) in [Infantry, Tank, Walker]:
        DICO_2A[key] = DICO_1A[key]
# For WEAPONS
for key in DICO_1A.keys():
    if type(DICO_1A[key]) in [Weapon]:
        DICO_2B[key] = DICO_1A[key]
# For COMPANIES
for key in DICO_1B.keys():
    if type(DICO_1B[key]) in [Company]:
        DICO_2C[key] = DICO_1B[key]
del DICO_1A , DICO_1B

# CSVs UNITS
fisrt_column_A = ["HP","ORG","SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack","Defense",
            "Breakthrought","Armor","Piercing","Hardness"]
DICO_3A["Units"] = fisrt_column_A
for key in DICO_2A.keys():
    cur = DICO_2A[key]
    assert type(cur) == Infantry or Tank or Walker
    cur_list = [cur.HP,cur.ORG,cur.SoftAttack,cur.HardAttack,cur.SoftMeleeAttack,cur.HardMeleeAttack,cur.Defense,
            cur.Breakthrought,cur.Armor,cur.Piercing,cur.Hardness]
    round_Stats(cur)
    DICO_3A[key] = cur_list

# CSVs WEAPONS
fisrt_column_B = ["SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack","Defense",
            "Breakthrought"]
DICO_3B["Weapons"] = fisrt_column_B
for key in DICO_2B.keys():
    cur = DICO_2B[key]
    assert type(cur) == Weapon
    cur_list = [cur.SoftAttack,cur.HardAttack,cur.SoftMeleeAttack,cur.HardMeleeAttack,cur.Defense,
            cur.Breakthrought]
    round_Stats(cur)
    DICO_3B[key] = cur_list

# CSVs COMPANIES
fisrt_column_C = ["HP","ORG","SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack","Defense",
            "Breakthrought","Armor","Piercing","Hardness"]
DICO_3C["Companies"] = fisrt_column_C
for key in DICO_2C.keys():
    cur = DICO_2C[key]
    assert type(cur) == Company
    cur_list = [cur.HP,cur.ORG,cur.SoftAttack,cur.HardAttack,cur.SoftMeleeAttack,cur.HardMeleeAttack,cur.Defense,
            cur.Breakthrought,cur.Armor,cur.Piercing,cur.Hardness]
    round_Stats(cur)
    DICO_3C[key] = cur_list

Dict2CSV(DICO_3A, "SaveUnit.csv")
Dict2CSV(DICO_3B, "SaveWeapons.csv")
Dict2CSV(DICO_3C, "SaveCompanies.csv")
