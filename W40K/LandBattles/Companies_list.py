from W40K.UnitCreator.Unit_list import *
from W40K.LandBattles.Company import Company

Guardsmens_100A = Company(Unit=Gardes.__copy__(100),
                          Equipement=[Lasgun.__copy__(95),
                                PlasmaGun.__copy__(5),
                                FragGrenades.__copy__(100),
                                KrakGrenades.__copy__(100)])

Spaces_100A = Company(Unit=SpaceMarines.__copy__(100),
                      Equipement=[Bolter.__copy__(90),
                            PlasmaGun.__copy__(5),
                            BolterLD.__copy__(5),
                            FragGrenades.__copy__(100),
                            KrakGrenades.__copy__(100)])