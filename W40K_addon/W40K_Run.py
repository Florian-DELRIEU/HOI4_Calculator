from W40K_addon.W40K_Unit import *
from W40K_addon.W40K_Company import *


BolterLD_1 = Weapon(5,4,"Lourde",Range=36,Cadence=3)
BolterLD_2 = BolterLD_1.__copy__()
CanonLaser = Weapon(9,1,"Lourde",Range=48,Cadence=1)

Predator = Tank(4,13,11,10,3,Quantity=1,Type="Tank")
Predator.setWeapons(
    TurretList=[CanonLaser],
    SideList=[BolterLD_1,BolterLD_2])