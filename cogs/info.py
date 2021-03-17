from discord.ext import commands
import time
import os
import os.path


class info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='sends the bots ping')
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")

    @commands.command(brief='gives the bots version')
    async def version(self, ctx):
        meow = open(os.path.join(os.path.dirname(__file__), os.pardir, 'version.txt'))
        await ctx.send(f'cheeseburger bot is running version {meow.read()}')


def setup(client):
    client.add_cog(info(client))
