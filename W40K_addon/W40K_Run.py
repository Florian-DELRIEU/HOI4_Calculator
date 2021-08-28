from W40K_addon.W40K_Unit import *
from W40K_addon.W40K_Company import *


SpaceMarines = Unit(4,4,4,4,1,1,8,3,None,100)
Bolter = Weapon(F=3,PA=5,Type="Tir Rapide",Quantity=100)
ReacteurDorsaux = Upgrade(BRK=1.5,Quantity = 20)

Comp = Company()
Comp.setUnit(SpaceMarines)
Comp.setEquipement([Bolter])
Comp.setUpgrade([ReacteurDorsaux])