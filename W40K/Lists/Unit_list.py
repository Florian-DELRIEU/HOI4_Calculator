from W40K.Class.Unit import Infantry, Tank, Walker
from W40K.Class.Weapons import Weapon
# Units
Gardes =        Infantry(3, 3, 3, 3, 1, 1, 7, 5, Name="Gardes")
SpaceMarines =  Infantry(4, 4, 4, 4, 1, 1, 9, 3, Name="Space Marines", SpecialRules=["Astartes"])

# Weapons
Lasgun = Weapon(3,None,Type="Tir rapide",Range=24,Name="Lasgun")
Bolter = Weapon(4,5,Type="Tir rapide",Range=24,Name="Bolter")
MeltaGun = Weapon(8,1,Type="Assaut",SpecialsRules=["Melta"],Range=12,Cadence=1)
PlasmaGun = Weapon(7,2,Type="Tir rapide",Range=24,Name="Plasma Gun",SpecialsRules=["Gets Hot"])
KrakGrenades = Weapon(6,4,Range=8,Type="Assaut",Cadence=1,SpecialsRules=["Krak Grenade"],Name="Krak Grenade")
FragGrenades = Weapon(3,None,Range=8,Type="Assaut",Cadence=1,SpecialsRules=["Blast 3'","Assault Grenade"],Name="Frag Grenade")
BolterLD = Weapon(5,4,Type="Lourde",Range=36,Cadence=3,Name="Bolter LD")
CanonLaser = Weapon(9,1,Type="Lourde",Range=48,Cadence=1,Name="Canon Laser")
Earthshaker = Weapon(9,3,Type="Ordnance",Range=240,SpecialsRules=["Barrage","Blast 5'"],Name="Earthshaker")
Obusier = Weapon(8,3,Range=72,Type="Ordnance",Cadence=1,SpecialsRules=["Blast 5'"],Name="Obusier")
Autocanon = Weapon(7,4,Range=48,Type="Lourde",Cadence=2,SpecialsRules=[],Name="Autocanon")

# CAC weapons
Astartes_CCW = Weapon(4,None,None,"Melee",Name="Astartes Knife")
Bayonet = Weapon(3,None,None,"Melee",Name="Lasgun bayonet")

# Vehicules and Artillerie
LemanRuss_A = Tank(3,14,12,10,3,Type="Heavy",Name="Leman Russ")
LemanRuss_A.setWeapons(
    TurretList=[Obusier.__copy__(1)],
    HullList=[BolterLD.__copy__(1)],
    SideList=[BolterLD.__copy__(2)])

Predator_A = Tank(4,13,11,10,3,Quantity=1,Type="Tank",Name="Predator")
Predator_A.setWeapons(
    TurretList=[Autocanon.__copy__(1)],
    HullList=[BolterLD.__copy__(1)],
    SideList=[BolterLD.__copy__(2)])

Basilisk = Tank(3,12,10,10,3,Type="Tank",SpecialRules=["Oppen-Topped"],Name="Basilisk")
Basilisk.setWeapons(
    TurretList=[Earthshaker.__copy__(1)],
    HullList=[BolterLD.__copy__(1)])

Field_Earthshaker = Tank(3,10,10,10,2,Type="Tank",SpecialRules=["Immobile"],Name="Earthshaker")
Field_Earthshaker.setWeapons(
    TurretList=[Earthshaker.__copy__(1)])

