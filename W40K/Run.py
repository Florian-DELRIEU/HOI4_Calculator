from W40K.LandBattles.Companies_list import *
from W40K.LandBattles.Company import Regiment
from W40K.LandBattles.Battle import Battle

RegA = Regiment(Name = "101st Regiment",
                CompagnieList = [
                        Guardsmens_100B,Guardsmens_100B,Guardsmens_100B,Guardsmens_100B,
                        Guardsmens_100B,Guardsmens_100B,Guardsmens_100C,Guardsmens_100C,
                ])
RegA.isDefending = True

RegB = Regiment(Name = "Ultramarines",
                CompagnieList = [
                        Spaces_100A,Spaces_100A,Spaces_100A,Spaces_100A
                ])

RegB.isDefending = False

BattleA = Battle(RegB,RegA)
BattleA.Round(-1)