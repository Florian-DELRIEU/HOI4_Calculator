from W40K_Unit import *
from W40K_Weapons import *
from W40K_Company import *
from W40K_Unit import *

Guards = Unit(Quantity=100)
Lasgun = Weapon(3,None,"Tir Rapide",Quantity=90,Name="Lasgun")
PlasmaGun = Weapon(7,2,"Tir Rapide",Quantity=5,Name="PlasmaGun")
BolterLD = Weapon(5,4,"Lourd",Quantity=5,Range=36,Name="Bolter Lourds")

Comp1 = Company()
Comp1.setUnit(Guards)
Comp1.setEquipement([Lasgun,PlasmaGun,BolterLD])