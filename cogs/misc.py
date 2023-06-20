import discord
from discord.ext import commands
from gtts import gTTS
import os
import importlib
import json
import time
from datetime import datetime


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
        myobj = gTTS(text=str(args), lang='ja', slow=False)
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

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def add_carrot(self, ctx):
        if ctx.guild.id != self.client.fwtarchiveserver:
            return
        if ctx.message.author.id not in self.client.owners:
            return
        if len(ctx.message.attachments) == 0:
            await ctx.send('u have to upload a pic first')
            return
        count = 1
        for _ in os.listdir('./content/images/carrots/'):
            count += 1
        os.system(f'curl "{ctx.message.attachments[0].url}" -s --output ./content/images/carrots/carrots{count}.png')
        await ctx.send('downloaded imag')
        self.client.cut_carrots.restart()

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def add_catgirl(self, ctx):
        if ctx.guild.id != self.client.fwtarchiveserver:
            return
        if ctx.message.author.id not in self.client.owners:
            return
        if len(ctx.message.attachments) == 0:
            await ctx.send('u have to upload a pic first')
            return
        os.system(f'curl "{ctx.message.attachments[0].url}" -s --output '
                  f'./content/images/catgirlmemes/{ctx.message.id}.png')
        await ctx.send('downloaded imag')
        self.client.catgirl_memes.restart()

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if guild.id == 896494939888824372:
            # Metallic and lime's IDs
            if member.id == 562765303092740096 or member.id == 963728309051605022:
                await member.guild.unban(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id == 963728309051605022:
            await member.add_roles(member.guild.get_role(898606840525504582))
        time.sleep(2)
        if member.id == 562765303092740096 or member.id == 963728309051605022:
            await member.remove_roles(member.guild.get_role(903102143932825620))


async def setup(client):
    await client.add_cog(misc(client))
