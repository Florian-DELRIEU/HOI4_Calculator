from Class.Battle import *
from Lib.DivisionList import *

# fixme Les tactics ne se choisissent pas

DivA = DivInfanterie36
DivA.is_defending = False
DivB = DivLightArmored36
DivB.is_defending = True

BATTLE = Battle(DivA,DivB)
BATTLE.run(-1)