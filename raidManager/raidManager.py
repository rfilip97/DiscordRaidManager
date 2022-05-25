
import asyncio
import os
import discord
import datetime

from raidManager.constants import NO_PLAYERS_SIGNED_STR
from raidManager.form import Form
from raidManager.raid import Raid
from raidManager.role import Role
from raidManager.raider import Raider
from utils.utils import message_check, get_emoji_list, list_to_str, get_formated_emoji, extract_emoji

TOKEN = os.getenv('DISCORD_TOKEN')
KEY = "!yk"

bot = discord.Client()


class RaidManager:

    channel = None
    form = None
    handler = None
    raid = Raid()
    server_emojis = None

    def __init__(self):
        pass

    def run(self):
        bot.run(TOKEN)

    async def dm(user, message):
        asyncio.create_task(user.send(message))

    async def react(emoji, emoji_list):
        emj = get_formated_emoji(emoji, emoji_list)
        await RaidManager.handler.add_reaction(emj)

    async def prepare_form(edit = False):

        form = Form(RaidManager.channel)
        form.addTitle(RaidManager.raid.getName())

        players = RaidManager.raid.getPlayers()
        roles = RaidManager.raid.getRoles()

        for role in roles:
            emoji = RaidManager.raid.getEmojiByRole(role)
            if emoji in RaidManager.server_emojis:
                emj = get_formated_emoji(emoji, RaidManager.server_emojis)
                emj = emj[:1] + ":" + emj[1:]

                players = RaidManager.raid.getPlayersByRole(role)
                if players != NO_PLAYERS_SIGNED_STR:
                    tmp_players = ""
                    for player in players:
                        tmp_players += player + "\n"
                    players = tmp_players

                form.addField("{}{}".format(emj, role), players)

        # Send the form
        if edit == False:
            RaidManager.handler = await form.publish()

            # React with the selected emojis
            for role in roles:
                emoji = RaidManager.raid.getEmojiByRole(role)
                await RaidManager.react(emoji, RaidManager.server_emojis)

        # Edit the form
        else:
            await RaidManager.handler.edit(embed=form.getEmbed())

    async def start_raid_form(message):
        author = message.author
        await RaidManager.dm(author, "Hey! Let's start filling the raid form ^^\nPlease submit raid title:")
        title = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

        RaidManager.channel = message.channel
        RaidManager.raid.setName(title.content)

        roles = ""
        await RaidManager.dm(author, "Enter [:emote:-role]. Type 'finish' to exit:")
        response = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

        emojis = []
        roles = []
        while response.content.lower() != "finish":
            response = response.content.split("-")
            emojis.append(response[0])
            roles.append(response[1])
            await RaidManager.dm(author, "Enter [:emote:-role]. Type 'finish' to exit:")
            response = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

        RaidManager.server_emojis = get_emoji_list(message)
        
        ct = 0
        for emoji in emojis:
            role = Role(roles[ct], emoji)
            RaidManager.raid.addRole(role)
            ct += 1

        RaidManager.raid.printRoles()
        await RaidManager.prepare_form()

##################
##### EVENTS #####
##################

### READY ###
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=KEY))

### MESSAGE REPLY ###
@bot.event
async def on_message(message):

    # make sure bot does not respond to itself
    if message.author == bot.user:
        return

    # Vars
    myid = "<@!" + str(bot.user.id) + ">"
    author_id = message.author.mention

    # commands
    if message.content.startswith(KEY + " "):

        words = message.content.split()

        ### raid formular ###
        # i.e. !yk start raid
        # i.e. !yk raid start
        if len(words) == 3:
            words[1] = words[1].lower()
            words[2] = words[2].lower()
            if ((words[1] == "start" and words[2] == "raid") or (words[1] == "raid" and words[2] == "start")):
                await RaidManager.start_raid_form(message)

### REACTION REPLY ###
@bot.event
async def on_reaction_add(reaction, user):
    # Ignore the reacts comming from the bot
    if user == bot.user:
        return

    if reaction.message.id == RaidManager.handler.id:
        emj = extract_emoji(str(reaction.emoji))
        raider = Raider(str(user))
        role = RaidManager.raid.getRoleByEmoji(emj)

        # Remove already existing player
        if str(user) in RaidManager.raid.roles[role].getPlayers():
            RaidManager.raid.removePlayer(str(user), role)
        # Add the player
        else:
            RaidManager.raid.addPlayer(raider, role)

        await RaidManager.prepare_form(edit=True)
