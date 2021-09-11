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

    roles = {}  # key: role.name, value: role

    def __init__(self, name=None, description=None, raidLeader=None, date=None, time=None, serverId=None, channelId=None):
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
        self.roles[role.getName()] = role

    def setName(self, name):
        self.name = name

    def getRoles(self):
        ret = []
        for role in self.roles:
           ret.append(role)
        return ret

    def getRoleByEmoji(self, emoji):
        for role in self.roles:
            if self.roles[role].emoji == emoji:
                return role
        return ""

    def getEmojiByRole(self, role):
        return self.roles[role].emoji

    def getPlayers(self):
        ret = []
        for role in self.roles:
            ret += self.roles[role].getPlayers()
        return ret

    def printRoles(self):
        for role in self.roles:
            print("-----------------")
            print("Role: " + role)
            print("Players:")
            self.roles[role].printPlayers()

    def addPlayer(self, player, role):
        if role not in self.roles:
            print("Invalid role: " + role)
            return
        print("Adding {} to {}".format(player.getName(), role))
        self.roles[role].addPlayer(player)

    def removePlayer(self, player, role):
        self.roles[role].removePlayer(player)
