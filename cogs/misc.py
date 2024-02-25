import discord
from discord.ext import commands
from gtts import gTTS
import importlib
import json

from utils import langgen


class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='says meow meow')
    async def meow(self, ctx):
        await ctx.message.channel.send('meow meow')

    @commands.command(brief='turns your text into a tts mp3')
    async def tts(self, ctx, *args):
        myobj = gTTS(text=str(args), lang='ja', slow=False)
        myobj.save("./content/tts.mp3")
        await ctx.send(file=discord.File('./content/tts.mp3'))

    @commands.command(brief='deletes the last message i sent')
    async def undo(self, ctx):
        # for i in await ctx.channel.history(limit=10).flatten():
        for i in await ctx.channel.history(limit=10):
            if i.author == self.client.user:
                await i.delete()
                break

    @commands.Cog.listener()
    async def on_error(self, ctx, exception):
        if "Missing Permissions" in str(exception):
            return await ctx.send(f'I dont have the permissions to use this command, consider giving the bot the'
                                  f' "Admin" permission')

    @commands.command()
    async def lang_gen(self, ctx):
        await ctx.send(langgen.generate_sentence(self.client.lang_gen_datatable))

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if str(ctx.command) == 'reload':
            with open('config.json') as file:
                owners = json.load(file)["owner-ids"]
            if ctx.author.id in owners:
                importlib.reload(langgen)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass


async def setup(client):
    await client.add_cog(misc(client))
