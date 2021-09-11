
import asyncio
import os
import discord
import random
import datetime
import random

from gw2.gw2 import Gw2
from discord.ext import commands
from raidManager.constants import NO_PLAYERS_SIGNED_STR
from raidManager.form import Form
from raidManager.raid import Raid
from raidManager.role import Role
from raidManager.raider import Raider
from utils.utils import message_check, get_emoji_list, list_to_str, get_formated_emoji, extract_emoji

TOKEN = os.getenv('DISCORD_TOKEN')
KEY = "!yk"

bot = discord.Client()


class Yukki:

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
        await Yukki.handler.add_reaction(emj)

    async def prepare_form(edit = False):

        form = Form(Yukki.channel)
        form.addTitle(Yukki.raid.getName())

        players = Yukki.raid.getPlayers()
        roles = Yukki.raid.getRoles()

        for role in roles:
            emoji = Yukki.raid.getEmojiByRole(role)
            if emoji in Yukki.server_emojis:
                emj = get_formated_emoji(emoji, Yukki.server_emojis)
                emj = emj[:1] + ":" + emj[1:]

                players = Yukki.raid.getPlayersByRole(role)
                if players != NO_PLAYERS_SIGNED_STR:
                    tmp_players = ""
                    for player in players:
                        tmp_players += player + "\n"
                    players = tmp_players

                form.addField("{}{}".format(emj, role), players)

        # Send the form
        if edit == False:
            Yukki.handler = await form.publish()

            # React with the selected emojis
            for role in roles:
                emoji = Yukki.raid.getEmojiByRole(role)
                await Yukki.react(emoji, Yukki.server_emojis)

        # Edit the form
        else:
            await Yukki.handler.edit(embed=form.getEmbed())

    async def start_raid_form(message):
        author = message.author
        await Yukki.dm(author, "Hey! Let's start filling the raid form ^^\nPlease submit raid title:")
        title = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

        Yukki.channel = message.channel
        Yukki.raid.setName(title.content)

        roles = ""
        await Yukki.dm(author, "Enter [:emote:-role]. Type 'finish' to exit:")
        response = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

        emojis = []
        roles = []
        while response.content.lower() != "finish":
            response = response.content.split("-")
            emojis.append(response[0])
            roles.append(response[1])
            await Yukki.dm(author, "Enter [:emote:-role]. Type 'finish' to exit:")
            response = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

        Yukki.server_emojis = get_emoji_list(message)
        
        ct = 0
        for emoji in emojis:
            role = Role(roles[ct], emoji)
            Yukki.raid.addRole(role)
            ct += 1

        Yukki.raid.printRoles()
        await Yukki.prepare_form()

### READY ###
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=KEY))

### REPLY ###
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

        ### GW2 ###
        # Dailies
        # i.e. "!yk dailies T4", "!yk dailies recommended"
        if len(words) == 3:
            words[1] = words[1].lower()
            words[2] = words[2].upper()
            accepted_words = ["T1", "T2", "T3", "T4", "RECOMMENDED"]
            if (words[1] == "dailies" or words[1] == "daily") and words[2] in accepted_words:
                tier = words[2]
                gw2 = Gw2()
                dailies = gw2.get_dailies(tier)

                if dailies == False:
                    await message.channel.send(author_id + " bad format. Try it like " + KEY + " dailies T4")
                    return

                else:
                    today = str(datetime.datetime.today())
                    today = str(today.split()[0])
                    embedVar = discord.Embed(
                        title="Fractal dailies of " + today, color=0x0066ff)
                    frac_str = ""
                    for daily in dailies:
                        frac_str += ":cyclone: " + daily + "\n"
                    embedVar.add_field(
                        name="Daily fractals " + tier, value=frac_str, inline=False)
                    await message.channel.send(embed=embedVar)
                    return

        ### raid formular ###
        # i.e. !yk start raid
        # i.e. !yk raid start
        if len(words) == 3:
            words[1] = words[1].lower()
            words[2] = words[2].lower()
            if ((words[1] == "start" and words[2] == "raid") or (words[1] == "raid" and words[2] == "start")):
                await Yukki.start_raid_form(message)

### REPLY ###
@bot.event
async def on_reaction_add(reaction, user):
    # Ignore the reacts comming from the bot
    if user == bot.user:
        return

    if reaction.message.id == Yukki.handler.id:
        emj = extract_emoji(str(reaction.emoji))
        raider = Raider(str(user))
        Yukki.raid.addPlayer(raider, Yukki.raid.getRoleByEmoji(emj))
        await Yukki.prepare_form(edit=True)