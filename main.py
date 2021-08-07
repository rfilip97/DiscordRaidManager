from raidManager.yukki import Yukki

yukki = Yukki()
yukki.run()


###############################
from raidManager.raid import Raid
from raidManager.raider import Raider
from raidManager.role import Role

# discordID, name
raider1 = Raider("#1111", "Kenny")
raider1.addRole("tank")
raider2 = Raider("#1234", "Ada")
raider2.addRole("dps")
raider2.addRole("tank")
raider3 = Raider("#1357", "Sonya")
raider3.setFlex(True)

# name, spots
role1 = Role("dps", "7")
role2 = Role("healer", "2")
role3 = Role("tank", "1")

# name, description, raidLeader, date, time, serverId
raid = Raid("Spirit Vale", "Training Run", "Yukki-kun",
            "12.04.2021", "18:00", "#1111", "#9999")
raid.addPlayer(raider1)
raid.addPlayer(raider2)
raid.addPlayer(raider3)
raid.addRole(role1)
raid.addRole(role2)
raid.addRole(role3)
