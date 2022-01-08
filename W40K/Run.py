from W40K.Lists.Companies_list import *
from W40K.Class.Regiment import Regiment
from W40K.Class.Battle import Battle

RegA = Regiment(Name = "101st Regiment",
                CompagnieList = [
                        Guardsmens_100B,Guardsmens_100B,Guardsmens_100B,Guardsmens_100B,
                        Guardsmens_100B,Guardsmens_100B,Guardsmens_100C,Guardsmens_100C,
                ])
RegA.isDefending = True

RegB = Regiment(Name = "Ultramarines",
                CompagnieList = [
                        Spaces_100A,Spaces_100A,Spaces_100A,Spaces_100A
                ],XP=100,Entrenchment_level=2)

RegB.isDefending = False

BattleA = Battle(RegB,RegA,Terrain="Plains",River=None)
BattleA.Round(-1)