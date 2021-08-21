from W40K_Unit import *

KrakGrenade = Weapon(8,2,"Assaut")
KrakGrenade.set_Quantity(100)

Lasgun = Weapon()
Lasgun.set_Quantity(100)
Lasgun.Show_HOI_Stats()


SpaceMarines = Unit(4,4,4,5,1,1,9,3)
SpaceMarines.set_Quantity(100)
SpaceMarines.Show_HOI_Stats()

Comp1 = Company()
Comp1.Unit = SpaceMarines
Comp1.Equipement = [Lasgun,KrakGrenade]
Comp1.Show_HOI_Stats()
