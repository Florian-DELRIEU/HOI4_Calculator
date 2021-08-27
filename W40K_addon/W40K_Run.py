from W40K_Unit import *
from W40K_Weapons import *
from W40K_Company import *
from W40K_Unit import *

BolterLD = Weapon(5,4,"Lourde",Range=36,Cadence=3)
CanonLaser = Weapon(9,1,"Lourde",Range=48,Cadence=1)

Predator = Tank(4,13,11,10,3,Quantity=1,Type="Tank")
Predator.setTurretWeapons([CanonLaser])
Predator.setSideWeapons([BolterLD,BolterLD])
