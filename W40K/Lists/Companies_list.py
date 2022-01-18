from W40K.Lists.Unit_list import *
from W40K.Class.Company import Company

Guardsmens_100A = Company(Unit=         Gardes.__copy__(100),
                          Equipement=[  Lasgun.__copy__(100),
                                        FragGrenades.__copy__(100)])

Guardsmens_100B = Company(Unit=         Gardes.__copy__(100),
                          Equipement=[  Lasgun.__copy__(100),
                                        FragGrenades.__copy__(100),
                                        KrakGrenades.__copy__(100)])

Guardsmens_100C = Company(Unit=         Gardes.__copy__(100),
                          Equipement=[  Lasgun.__copy__(90),
                                        PlasmaGun.__copy__(5),
                                        BolterLD.__copy__(6),
                                        FragGrenades.__copy__(60),
                                        KrakGrenades.__copy__(40),
                                        Bayonet.__copy__(100)])

Spaces_Tactical = Company(Unit=     SpaceMarines.__copy__(100),
                      Equipement=[  Bolter.__copy__(85),
                                    PlasmaGun.__copy__(5),
                                    CanonLaser.__copy__(2),
                                    MeltaGun.__copy__(3),
                                    BolterLD.__copy__(5),
                                    FragGrenades.__copy__(100),
                                    KrakGrenades.__copy__(100),
                                    Astartes_CCW.__copy__(100)])

Spaces_Devastator = Company(Unit=   SpaceMarines.__copy__(100),
                      Equipement=[  Bolter.__copy__(50),
                                    PlasmaGun.__copy__(10),
                                    CanonLaser.__copy__(5),
                                    MeltaGun.__copy__(5),
                                    BolterLD.__copy__(25),
                                    FragGrenades.__copy__(100),
                                    KrakGrenades.__copy__(100),
                                    Astartes_CCW.__copy__(50)])

Spaces_Assault = Company(Unit=      SpaceMarines.__copy__(100),
                      Equipement=[  BoltPistol.__copy__(90),
                                    PlasmaPistol.__copy__(10),
                                    MeltaBomb.__copy__(10),
                                    FragGrenades.__copy__(100),
                                    KrakGrenades.__copy__(100),
                                    Astartes_CCW.__copy__(100)],
                      Upgrade=[Upgrade(Name="Jump Pack",BRK=1.3,Quantity=100)])

Basilisk_15A = Company(Unit= Basilisk.__copy__(15))

Predator_9A = Company(Unit= Predator_A.__copy__(9))

Earthshaker_Company = Company(Unit=Field_Earthshaker.__copy__(12))