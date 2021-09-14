from W40K.LandBattles.Companies_list import *
from W40K.LandBattles.Company import Regiment
from W40K.LandBattles.Battle import Battle

RegA = Regiment([Guardsmens_100A,Guardsmens_100A,Guardsmens_100A,Guardsmens_100A],"101st Regiment")
RegA.isDefending = True

RegB = Regiment([Spaces_100A,Spaces_100A],"Ultramarines")
RegB.isDefending = False

BattleA = Battle(RegB,RegA)
BattleA.Round(-1)