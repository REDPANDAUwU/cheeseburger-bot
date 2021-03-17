from discord.ext import commands
import discord
import time
import os
import os.path
import git

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
    async def info(self, ctx):
        repo = git.Repo('/home/gaming/cheeseburger-bot/')
        commits = repo.git.rev_list('--count', 'HEAD')
        embedz = discord.Embed(title='bot info', description=str(commits), color=0x00ff00)
        embedz.set_thumbnail(url=self.client.avatar_url)
        await ctx.send(embed=embedz)


def setup(client):
    client.add_cog(info(client))
