from W40K.Class.Unit import Infantry

from W40K.Lists.Weapons_list import *
from W40K.Lists.CAC_Weapons_list import *

# Units
Gardes =        Infantry(3, 3, 3, 3, 1, 1, 7, 5, Name="Gardes")
SpaceMarines =  Infantry(4, 4, 4, 4, 1, 1, 9, 3, Name="Space Marines", SpecialRules=["Astartes"])
