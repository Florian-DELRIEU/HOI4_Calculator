from Class.Battle import *
from Lib.DivisionList import *

DivA = DivInfanterie36
DivA.is_defending = False
DivB = DivLightArmored36
DivB.is_defending = True

BATTLE = Battle(DivA,DivB)
BATTLE.run_rounds(-1)