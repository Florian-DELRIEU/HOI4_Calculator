from W40K_Unit import *
from W40K_Weapons import *
from W40K_Company import *
from W40K_Unit import *

Bolter = Weapon(4,5,"Tir rapide")
PlasmaGun = Weapon(7,2,"Tir Rapide")
SpaceMarines = Unit(4,4,4,5,1,1,7,3)


Comp1 = Company()
SpaceMarines.set_Quantity(100)
Bolter.set_Quantity(100)
Comp1.setUnit(SpaceMarines)
Comp1.setEquipement([Bolter])

Comp2 = Company()
Bolter.set_Quantity(95)
Comp2.setUnit(SpaceMarines)
Comp2.setEquipement([Bolter,PlasmaGun])


Comp1.Show_HOI_Stats()
Comp2.Show_HOI_Stats()
