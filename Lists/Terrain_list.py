from W40K.Class.Terrain import Terrain

Terrain_dico = {
    "Plains": Terrain((90,45),Attrition=0,AttackMalus=1,AirSuperiorityMalus=1),
    "Desert": Terrain((90,45),Attrition=.2,AttackMalus=1,AirSuperiorityMalus=1),
    "Forest": Terrain((84,42),Attrition=0,AttackMalus=0.8,AirSuperiorityMalus=0.9),
    "Hills": Terrain((80,40),Attrition=0,AttackMalus=0.7,AirSuperiorityMalus=-0.95),
    "Jungle": Terrain((84,42),Attrition=0.3,AttackMalus=0.7,AirSuperiorityMalus=0.75),
    "Marsh": Terrain((78,26),Attrition=0.5,AttackMalus=0.6,AirSuperiorityMalus=1),
    "Moutain": Terrain((75,25),Attrition=0.4,AttackMalus=0.4,AirSuperiorityMalus=0.9),
    "Urban": Terrain((96,32),Attrition=0,AttackMalus=0.7,AirSuperiorityMalus=0.5),
}