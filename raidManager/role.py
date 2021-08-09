class Role:

    name = None
    spots = None
    players = None    # key: player.name, value: player

    def __init__(self, name, spots):
        self.name = name
        self.spots = spots
        self.players = {}

    def getName(self):
        return self.name

    def getSpots(self):
        return self.spots

    def addPlayer(self, player):
        if player.getName() not in self.players:
            self.players[player.getName()] = player

    def removePlayer(self, player):
        if player in self.players:
            print("removed {} from {}".format(player, self.name))
            del self.players[player]

    def printPlayers(self):
        for player in self.players:
            print(player)
