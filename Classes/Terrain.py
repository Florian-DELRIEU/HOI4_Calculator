class Terrain:
    def __init__(self, name, width):
        self.name = name
        self.width = width

    def get(self):
        return {
            "name": self.name,
            "width": self.width
        }