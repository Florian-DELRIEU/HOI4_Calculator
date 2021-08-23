from W40K_Unit import *
from W40K_Weapons import *
from W40K_Company import *
from W40K_Unit import *

Bolter = Weapon(4,5,"Tir rapide")
SpaceMarines = Unit(4,4,4,5,1,1,9,3)

print("Lasgun stats --")
Bolter.Show_HOI_Stats()
print("Space Marine stats --")
SpaceMarines.Show_HOI_Stats()
