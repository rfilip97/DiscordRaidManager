from raidManager import raider
from raidManager import role


class Raid:

    name = None
    description = None
    raidLeader = None
    date = None
    time = None
    serverId = None
    channelId = None

    roles = []
    players = []

    def __init__(self, name, description, raidLeader, date, time, serverId, channelId):
        self.name = name
        self.description = description
        self.raidLeader = raidLeader
        self.date = date
        self.time = time
        self.serverId = serverId
        self.channelId = channelId

    def getName(self):
        return self.name

    def addRole(self, role):
        self.roles.append(role)

    def addPlayer(self, player):
        self.players.append(player)
