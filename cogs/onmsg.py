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

        # this is for getting data for the lang_gen command

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

        # dotbot

        if message.content == '.' and message.channel.name == 'dot-wars':  # TODO: make this toggleable per server
            role = get(message.guild.roles, name="Dot Master!")

            await message.author.add_roles(role)

            for i in message.guild.members:
                if role in i.roles and i != message.author:
                    await i.remove_roles(role)

        elif message.channel.name == 'dot-wars' and message.content != '.':
            await message.delete()

        if message.author == self.client.user:
            return

        # cheeseburger chat 69 chat
        if message.channel.id == 782825184054476821:
            if '69' not in message.content.split():
                await message.delete()

        # react to burger and cheese

        if message.content.lower().startswith('burger') or message.content.lower().startswith('cheese'):
            emoji = '<cheeseburger:821355767436804116>'
            await message.add_reaction(emoji)
            emoji = '<:CRAB_IS_DANCE:821355752773517342>'
            await message.add_reaction(emoji)

        # darwin quotes

        if message.author.id == 203277749912076288:
            quote_channel = self.client.get_channel(775250281998319676)
            attachments = message.attachments
            if len(attachments) == 0:
                await quote_channel.send(
                    "'" + discord.utils.escape_mentions(message.content) + "' - darwin, " + str(message.created_at))
            elif len(attachments) == 1:
                await quote_channel.send(
                    "'" + discord.utils.escape_mentions(message.content) + "' - darwin, " + str(
                        message.created_at) + "\n" +
                    attachments[0].url)
            else:
                await quote_channel.send(
                    "'" + discord.utils.escape_mentions(message.content) + "' - darwin, " + str(message.created_at))
                for image in range(len(attachments)):
                    await quote_channel.send(attachments[image - 1].url)

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
    async def on_reaction_add(self, reaction, user):  # TODO: make this toggleable per server
        try:
            await reaction.message.add_reaction(reaction)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):  # TODO: make this server universal
        if before.channel.id == 782825184054476821:
            msg = after.content.split()
            dont_delete = False
            for i in msg:
                if i == '69':
                    dont_delete = True
            if not dont_delete:
                await before.delete()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        # print('super epic')
        # print(ctx.command)
        if str(ctx.command) == 'reload':
            with open('config.json') as file:
                owners = json.load(file)["owner-ids"]
            if ctx.author.id in owners:
                importlib.reload(langgen)


async def setup(client):
    await client.add_cog(onmsg(client))
