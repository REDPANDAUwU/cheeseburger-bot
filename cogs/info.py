from discord.ext import commands
import discord
import time
import os
import os.path
from git import Repo


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

    @commands.command(brief='gives basic info on the bot')
    async def about(self, ctx):
        embedz = discord.Embed(title='bot info', description='da best bot eva made', color=0x00ff00)
        embedz.add_field(name="source", value='https://github.com/REDPANDAUwU/cheeseburger-bot')
        embedz.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embedz)

    @commands.command(brief='gives invite for the bot')
    async def invitelink(self, ctx):
        ctx.send(f'https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot')


def setup(client):
    client.add_cog(info(client))
