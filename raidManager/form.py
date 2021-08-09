import discord


class Form:

    ctx = None
    embed = None

    def __init__(self, ctx):
        self.ctx = ctx

    def addTitle(self, title):
        self.embed = discord.Embed(title=title, color=0x0066ff)

    def addField(self, name, value):
        self.embed.add_field(name=name, value=value, inline=False)

    async def publish(self):
        await self.ctx.channel.send(embed=self.embed)
