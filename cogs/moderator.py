import io
import json
import os
import sys
import time

import aiohttp
import discord
# from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
import contextlib
import importlib

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/utils")
import fwtarchive
import dmall


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def fwtarchive(self, ctx):
        if ctx.author.id not in self.client.owners:
            return
        if ctx.channel.guild.id != self.client.fwtarchiveserver:
            return
        await fwtarchive.fwtarchive(self, ctx.channel, False)

    @fwtarchive.error
    async def fwtarchive_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def dmall(self, ctx):
        await dmall.dmall(self, ctx)

    @commands.command()
    async def execute(self, ctx, *, code):
        if ctx.author.id not in self.client.owners:
            await ctx.send('shut up')
            return
        str_obj = io.StringIO()
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
        await ctx.send(f'```{str_obj.getvalue()}```')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        # print('super epic')
        # print(ctx.command)
        if str(ctx.command) == 'reload':
            with open('config.json') as file:
                owners = json.load(file)["owner-ids"]
            if ctx.author.id in owners:
                importlib.reload(dmall)


async def setup(client):
    await client.add_cog(Moderator(client))
