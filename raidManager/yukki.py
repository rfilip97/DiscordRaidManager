from collections.abc import Sequence
import asyncio
import os
import discord
import random
import datetime
import random

from gw2.gw2 import Gw2
from discord.ext import commands
from raidManager.form import Form

TOKEN = os.getenv('DISCORD_TOKEN')
KEY = "!yk"

bot = discord.Client()


class Yukki:

    def __init__(self):
        pass

    def run(self):
        bot.run(TOKEN)


### READY ###
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=KEY))


### Aux ###
def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)


def message_check(channel=None, author=None, content=None):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)

    def check(message):
        if message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content
        if content and actual_content not in content:
            return False
        return True
    return check


### Commands ###
async def dm(user, message):
    asyncio.create_task(user.send(message))


async def start_raid_form(message):
    author = message.author
    await dm(author, "Hey! Let's start filling the raid form ^^\nPlease submit raid title:")
    title = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

    form = Form(message)
    form.addTitle(title.content)

    roles = ""
    await dm(author, "Enter [:emote:-role]. Type 'finish' to exit:")
    response = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))
    while response.content.lower() != "finish":

        response = response.content.split("-")
        roles += response[0] + " -> " + response[1]
        roles += "\n"
        await dm(author, "Enter [:emote:-role]. Type 'finish' to exit:")
        response = await bot.wait_for('message', check=message_check(channel=message.author.dm_channel))

    form.addField("roles", roles)
    await form.publish()


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
                await start_raid_form(message)
