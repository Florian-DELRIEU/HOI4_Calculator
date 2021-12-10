from W40K.Class.Unit import Tank, Walker

from W40K.Lists.CAC_Weapons_list import *
from W40K.Lists.Weapons_list import *

LemanRuss_A = Tank(3,14,12,10,3,Type="Heavy")
LemanRuss_A.setWeapons(
    TurretList=[Obusier.__copy__(1)],
    HullList=[BolterLD.__copy__(1)],
    SideList=[BolterLD.__copy__(2)])

Predator_A = Tank(4,13,11,10,3,Quantity=1,Type="Tank")
Predator_A.setWeapons(
    TurretList=[Autocanon.__copy__(1)],
    HullList=[BolterLD.__copy__(1)],
    SideList=[BolterLD.__copy__(2)])

Basilisk = Tank(3,12,10,10,3,Type="Tank")
Basilisk.setWeapons(
    TurretList=[Earthshaker.__copy__(1)],
    HullList=[BolterLD.__copy__(1)])

Field_Earthshaker = Tank(3,11,11,11,3,Type="Tank")
Field_Earthshaker.setWeapons(
    TurretList=[Earthshaker.__copy__(1)],
    HullList=[BolterLD.__copy__(1)])
