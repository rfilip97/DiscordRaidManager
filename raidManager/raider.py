from raidManager import constants


class Raider:

    discordID = None
    name = None
    desiredRoles = []
    flex = None

    def __init__(self, discordID, name, roles, flex=False):
        self.discordID = discordID
        self.name = name
        self.flex = flex
        self.desiredRoles = roles.split(constants.DELIM)

    def getName(self):
        return self.name

    def isFlex(self):
        return self.flex

    def getDesiredRoles(self):
        return self.desiredRoles

    def countRoles(self):
        return len(self.desiredRoles)
