from W40K_UnitCreator import *

Lasgun = Weapon()
Lasgun.set_Quantity(100)
Lasgun.Show_HOI_Stats()

SpaceMarines = Unit(4,4,4,5,1,1,9,3)
SpaceMarines.set_Quantity(100)
SpaceMarines.Show_HOI_Stats()

Comp1 = Company()
Comp1.Unit = SpaceMarines
Comp1.Equipement = [Lasgun]
Comp1.Show_HOI_Stats()