from W40K.UnitCreator.Class.Unit import Infantry, Tank, Walker
from W40K.UnitCreator.Class.Weapons import Weapon

# Units
Gardes =        Infantry(3, 3, 3, 3, 1, 1, 7, 5, Name="Gardes")
SpaceMarines =  Infantry(4, 4, 4, 4, 1, 1, 9, 3, Name="Space Marines", SpecialRules=["And they shall know no fear"])
LemanRuss = Tank(3,14,12,10,3,Type="Heavy")
Predator = Tank(4,13,11,10,3,Quantity=1,Type="Tank")

# Weapons
Lasgun = Weapon(3,None,"Tir rapide",24,Name="Lasgun")
Bolter = Weapon(4,5,"Tir rapide",24,Name="Bolter")
PlasmaGun = Weapon(7,2,"Tir rapide",24,Name="Plasma Gun")
KrakGrenades = Weapon(6,4,"Assaut",Range=8,Cadence=1,SpecialsRules=["Krak Grenade"],Name="Krak Grenade")
FragGrenades = Weapon(3,None,"Assaut",Range=8,Cadence=1,SpecialsRules=["Blast 3'"],Name="Frag Grenade")
BolterLD = Weapon(5,4,"Lourde",Range=36,Cadence=3,Name="Bolter LD")
CanonLaser = Weapon(9,1,"Lourde",Range=48,Cadence=1,Name="Canon Laser")


#### testing
KrakGrenadesA = Weapon(6,4,"Assaut",Range=8,Cadence=1,SpecialsRules=["Krak Grenade"],Name="Krak Grenade")
KrakGrenadesB = KrakGrenadesA.__copy__(100)