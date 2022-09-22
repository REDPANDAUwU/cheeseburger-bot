from discord.ext import commands
import discord
import time
import os
import os.path
import speedtest


def bytesto(_bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    r = float(_bytes)
    for i in range(a[to]):
        r = r / bsize

    return r


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
        embedz.set_thumbnail(url=self.client.user.avatar)
        await ctx.send(embed=embedz)

    @commands.command(brief='gives invite for the bot')
    async def invitelink(self, ctx):
        await ctx.send(f'https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope'
                       f'=bot')

    @commands.command(brief='gives the bots upload and download speed', name='speedtest')
    async def _s_peedt_est(self, ctx):
        await ctx.send('doing speedtest...')
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        await ctx.send(f'download: {round(bytesto(res["download"], "m"))} MB/s '
                       f'\nupload: {round(bytesto(res["upload"], "m"))} MB/s'
                       f'\nping: {round(res["ping"])} Milliseconds')


async def setup(client):
    await client.add_cog(info(client))
