from raidManager import constants


class Raider:

    discordID = None
    name = None
    desiredRoles = []
    flex = False

    def __init__(self, discordID, name):
        self.discordID = discordID
        self.name = name

    def getName(self):
        return self.name

    def isFlex(self):
        return self.flex

    def getDesiredRoles(self):
        return self.desiredRoles

    def countRoles(self):
        return len(self.desiredRoles)

    def addRole(self, role):
        self.desiredRoles.append(role)

    def setFlex(self, flex):
        self.flex = flex
