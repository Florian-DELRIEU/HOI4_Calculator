from MyPack.Convert import Dict2CSV
import W40K.UnitCreator.Main_Converter as main
from W40K.UnitCreator.Class.Unit import Infantry,Tank,Walker
from W40K.UnitCreator.Class.Weapons import Weapon


DICO_1 = main.__dict__    # toutes les variables et classes de main dans un dico
DICO_2 = dict()           # Pour les sauvegardes

for key in DICO_1.keys():
    if type(DICO_1[key]) in [Weapon, Infantry, Tank, Walker]:
        DICO_2[key] = DICO_1[key]

DICO_1 = DICO_2
del DICO_2
