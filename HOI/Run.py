from Class import *
from DivisionList import DIVISION_DICT

DivA = DIVISION_DICT["Infantry_72"]
DivA.is_defending = False
DivB = DIVISION_DICT["Armored_432"]
DivB.is_defending = True

BATTLE = Battle(DivA,DivB)
BATTLE.run_rounds(-1)