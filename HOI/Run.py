from Class import *
from DivisionList import Div_Dico

DivA = Div_Dico["Infantry_72"]
DivA.is_defending = False
DivB = Div_Dico["Armored_432"]
DivB.is_defending = True

BATTLE = Battle(DivA,DivB)
BATTLE.Round(-1)