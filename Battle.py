from LandBattleCalculator import *
from DivisionList import *

DivA = Infantery_72
DivA.isDefending = False
DivB = Armored_432
DivB.isDefending = True

BATTLE = Battle(DivA,DivB)
BATTLE.Round(-1)