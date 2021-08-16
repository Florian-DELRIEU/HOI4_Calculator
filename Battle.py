from LandBattleCalculator import *

DivA = Division()
DivA.isDefending = False
DivB = Division()
DivB.isDefending = True

BATTLE = Battle(DivA,DivB)
BATTLE.Round(-1)