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
                          Equipement=[  Lasgun.__copy__(85),
                                        PlasmaGun.__copy__(5),
                                        BolterLD.__copy__(10),
                                        FragGrenades.__copy__(100),
                                        KrakGrenades.__copy__(100),
                                        Bayonet.__copy__(100)])

Spaces_100A = Company(Unit=         SpaceMarines.__copy__(100),
                      Equipement=[  Bolter.__copy__(85),
                                    PlasmaGun.__copy__(5),
                                    CanonLaser.__copy__(2),
                                    MeltaGun.__copy__(3),
                                    BolterLD.__copy__(5),
                                    FragGrenades.__copy__(100),
                                    KrakGrenades.__copy__(100)])

Spaces_100B = Company(Unit= SpaceMarines.__copy__(100),
                      Equipement=[  Bolter.__copy__(85),
                                    PlasmaGun.__copy__(5),
                                    CanonLaser.__copy__(2),
                                    MeltaGun.__copy__(3),
                                    BolterLD.__copy__(5),
                                    FragGrenades.__copy__(100),
                                    KrakGrenades.__copy__(100),
                                    Astartes_CCW.__copy__(100)])

Basilisk_40A = Company(Unit= Basilisk.__copy__(40))