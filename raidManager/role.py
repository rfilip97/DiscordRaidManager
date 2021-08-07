class Role:

    name = None
    spots = None

    def __init__(self, name, spots):
        self.name = name
        self.spots = spots

    def getName(self):
        return self.name

    def getSpots(self):
        return self.spots
