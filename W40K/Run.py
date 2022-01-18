from W40K.Lists.Companies_list import *
from W40K.Class.Regiment import Regiment
from W40K.Class.Battle import Battle
from W40K.Class.Leader import Leader

RegA = Regiment(Name = "101st Regiment",
                CompagnieList = [
                        Guardsmens_100C,Guardsmens_100C,Guardsmens_100C,
                        Guardsmens_100C,Guardsmens_100C,Guardsmens_100C,
                        Basilisk_15A,Basilisk_15A,
                ])
RegA.isDefending = True

RegB = Regiment(Name = "Ultramarines",
                CompagnieList = [
                        Spaces_Tactical,Spaces_Tactical,Spaces_Tactical,
                        Spaces_Tactical,Spaces_Tactical,Spaces_Tactical,
                        Spaces_Devastator,Spaces_Devastator,

                ],XP=100,Entrenchment_level=2)

RegB.isDefending = False

BattleA = Battle(RegB,RegA,ATK_leader=Leader(1,3,1,["Assaut"],[]),DEF_leader=Leader(1,1,1,[],[]),Terrain="Plains",River=None)
BattleA.Round(-1)