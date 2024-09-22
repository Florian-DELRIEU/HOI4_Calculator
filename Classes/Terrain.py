class Terrain:
    def __init__(self, name, attack, width, extra_width, air_support):
        #todo add on GUI:
        #   + river
        #   + other side
        #   o Paradrop ?
        #   o Naval invasion

        self.name = name
        self.attack = attack
        self.width = width
        self.extra_width = extra_width
        self.has_small_river = False
        self.has_large_river = False
        self.air_support = air_support #todo no effect for now

    def get(self):
        return {
            "name": self.name,
            "attack": self.attack,
            "width": self.width,
            "extra_width": self.extra_width,
            "has_small_river": self.has_small_river,
            "has_large_river": self.has_large_river,
        }

    def __repr__(self):
        return self.name