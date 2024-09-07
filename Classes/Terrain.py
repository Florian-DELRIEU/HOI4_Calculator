class Terrain:
    def __init__(self, name, width):
        #todo add on GUI:
        #   - river
        self.name = name
        self.width = width
        self.has_river = False

    def get(self):
        return {
            "name": self.name,
            "width": self.width
        }

    def __repr__(self):
        return self.name