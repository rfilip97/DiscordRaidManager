import discord


class Form:

    channel = None
    embed = None

    def __init__(self, channel):
        self.channel = channel

    def addTitle(self, title):
        self.embed = discord.Embed(title=title, color=0x0066ff)

    def addField(self, name, value):
        self.embed.add_field(name=name, value=value, inline=False)

    async def publish(self):
        handler = await self.channel.send(embed=self.embed)
        return handler
