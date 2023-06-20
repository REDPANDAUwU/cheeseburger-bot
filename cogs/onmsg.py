import discord
from discord.ext import commands
from discord.utils import get
import sys
import os
import random
import importlib
import json

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/utils")
import dmall
from utils import langgen


class onmsg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            return

        if message.channel.id == 896496646773424178 and message.content != '' \
                and message.author.id != self.client.user.id and str(message.author.discriminator) != "0000":
            self.client.write_queue.append(message.content)
            if len(self.client.write_queue) > 10:
                for m in self.client.write_queue:
                    log_file = open('input.txt', 'a')
                    log_file.write(f'{m}\n')
                    log_file.close()
                self.client.write_queue = []

            r = random.randint(0, 15)
            # print(r)
            if r == 6:
                await message.channel.send(langgen.generate_sentence(self.client.lang_gen_datatable))

        if message.author == self.client.user:
            return

        # react to burger and cheese moduel

        if message.content.lower().startswith('burger') or message.content.lower().startswith('cheese'):
            emoji = '<cheeseburger:821355767436804116>'
            await message.add_reaction(emoji)
            emoji = '<:CRAB_IS_DANCE:821355752773517342>'
            await message.add_reaction(emoji)

        # darwin quotes

        # let GenAi bot use the dmall command (because funny)
        # discord.py by default blocks command requests from bots so i need to do this
        if message.author.id == 656962312565030963 or message.author.id == 694482209096204308:
            if message.content.lower().startswith(f'{self.client.prefix}dmall'):
                ctx = await self.client.get_context(message)
                await dmall.dmall(self, ctx, True)

        ctx = await self.client.get_context(message)

        if ctx.valid and str(ctx.author)[::-1][:5][::-1] == "#0000":
            await self.client.invoke(ctx)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        # print('super epic')
        # print(ctx.command)
        if str(ctx.command) == 'reload':
            with open('config.json') as file:
                owners = json.load(file)["owner-ids"]
            if ctx.author.id in owners:
                importlib.reload(langgen)

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #    if member.id == 552225393571004425 and member.guild.id == 690036880812671048:
    #        await member.ban()


async def setup(client):
    await client.add_cog(onmsg(client))
