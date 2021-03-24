import discord
from discord.ext import commands
import json
import aiohttp
from discord import Webhook, AsyncWebhookAdapter
from gtts import gTTS
import random


class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='says the infamous logan')
    async def theinfamouslogan(self, ctx):
        await ctx.message.channel.send('theinfamouslogan')

    @commands.command(brief='says meow meow')
    async def meow(self, ctx):
        await ctx.message.channel.send('meow meow')

    @commands.command(brief='turns your text into a tts mp3')
    async def tts(self, ctx, *args):
        myobj = gTTS(text=str(args), lang='en', slow=False)
        myobj.save("./content/tts.mp3")
        await ctx.send(file=discord.File('./content/tts.mp3'))

    @commands.command(brief='hot esex')
    async def esex(self, ctx):
        if ctx.message.author.id == 552225393571004425:
            await ctx.message.channel.send('michel wilde sex time pogpgopgogpg !!  !  !! !!! ! !!!!!!!!')
        else:
            await ctx.message.channel.send('chewseburger bot puts its hot penis inside ur hot boy pussy hehehe')

    @commands.command(brief='deletes the last message i sent')
    async def undo(self, ctx):
        for i in await ctx.channel.history(limit=10).flatten():
            if i.author == self.client.user:
                await i.delete()
                break

    @commands.Cog.listener()
    async def on_error(self, ctx, exception):
        if "Missing Permissions" in str(exception):
            return await ctx.send(f'I dont have the permissions to use this command, consider giving the bot the'
                                  f' "Admin" permission')


def setup(client):
    client.add_cog(misc(client))
