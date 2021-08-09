from raidManager import constants


class Raider:

    discordID = None
    name = None
    flex = False

    def __init__(self, discordID, name):
        self.discordID = discordID
        self.name = name

    def getName(self):
        return self.name

    def isFlex(self):
        return self.flex

    def setFlex(self, flex):
        self.flex = flex
