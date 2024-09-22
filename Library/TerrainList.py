from Classes import Terrain

Terrain = Terrain.Terrain

class Terrain_name(enumerate):
        Desert = "Desert"
        Forest = "Forest"
        Hills = "Hills"
        Jungle = "Jungle"
        Marsh = "Marsh"
        Moutain = "Moutain"
        Plains = "Plains"
        Urban = "Urban"

terrain_list = [
    Terrain(Terrain_name.Desert,
            width=70,
            extra_width=35,
            attack=0,
            air_support=0
            ),
    Terrain(Terrain_name.Forest,
            width=60,
            extra_width=30,
            attack= -0.15,
            air_support=-0.1
            ),
    Terrain(Terrain_name.Hills,
            width=75,
            extra_width=35,
            attack= -0.25,
            air_support=-0.05
            ),
    Terrain(Terrain_name.Jungle,
            width=60,
            extra_width=30,
            attack= -0.30,
            air_support=-0.25
            ),
    Terrain(Terrain_name.Marsh,
            width=50,
            extra_width=25,
            attack= -0.40,
            air_support=-0.25
            ),
    Terrain(Terrain_name.Moutain,
            width=50,
            extra_width=25,
            attack= -0.50,
            air_support=-0.10
            ),
    Terrain(Terrain_name.Plains,
            width=70,
            extra_width=35,
            attack= 0,
            air_support= 0
            ),
    Terrain(Terrain_name.Urban,
            width=80,
            extra_width=40,
            attack= -0.40,
            air_support=-0.50
            ),
]