from W40K_addon.W40K_saved import *
from W40K_addon.W40K_Company import *
from W40K_addon.W40K_Battle import *

CompA = Company(Unit=Gardes.__copy__(100),
                Equipement=[Lasgun.__copy__(95),
                            PlasmaGun.__copy__(5),
                            FragGrenades.__copy__(100),
                            KrakGrenades.__copy__(100)])
RegA = Regiment([CompA,CompA],"101st Regiment")

CompB = Company(Unit=SpaceMarines.__copy__(100),
                Equipement=[Bolter.__copy__(90),
                            PlasmaGun.__copy__(5),
                            BolterLD.__copy__(5),
                            FragGrenades.__copy__(100),
                            KrakGrenades.__copy__(100)])
RegB = Regiment([CompB,CompB],"Ultramarines")
RegB.isDefending = False

BattleA = Battle(RegB,RegA)
BattleA.Round(-1)