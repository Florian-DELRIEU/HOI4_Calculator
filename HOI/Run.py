from Class import *
from DivisionList import Div_Dico

DivA = Div_Dico["Infantry_72"]
DivA.isDefending = False
DivB = Div_Dico["Armored_432"]
DivB.isDefending = True

BATTLE = Battle(DivA,DivB)
BATTLE.Round(-1)