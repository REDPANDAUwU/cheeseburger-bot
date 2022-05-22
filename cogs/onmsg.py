import discord
from discord.ext import commands
from discord.utils import get
import sys
import os
import random

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

        if message.channel.id == 896496646773424178 and message.content != '':
            with open('input.txt', 'a+') as text_file:
                # print('seexx')
                text_file.write(f'{message.content}\n')
                text_file.close()
            r = random.randint(0, 15)
            # print(r)
            if r == 6:
                await message.channel.send(langgen.generate_sentence())

        # dotbot
        if message.content == '.' and message.channel.name == 'dot-wars':
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
            msg = message.content.split()
            dont_delete = False
            for i in msg:
                if i == '69':
                    dont_delete = True
            if not dont_delete:
                await message.delete()

        # megagamer lisp

        if message.author.id == 510647816700428289:
            # print('meow')
            lisp = ''
            do_lisp = False
            for i in message.content:
                if i == 's' or i == 'z' or i == 'S' or i == 'Z':
                    i = 'th'
                    do_lisp = True
                lisp += i
            if not do_lisp:
                return
            characters = 0
            for _ in lisp:
                characters += 1
            if characters > 2000:
                await message.channel.send('stfu megagamer')
            else:
                await message.channel.send(discord.utils.escape_mentions(lisp))

        # react to burger and cheese moduel

        if message.content.startswith('burger') or message.content.startswith('cheese') or message.content.startswith(
                'Burger') or message.content.startswith('Cheese'):
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
                await dmall.dmall(self, message, message.content[6:].split(), True)

        ctx = await self.client.get_context(message)

        if ctx.valid and str(ctx.author)[::-1][:5][::-1] == "#0000":
            await self.client.invoke(ctx)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.guild.id != 828797783863591012:
            try:
                await reaction.message.add_reaction(reaction)
            except discord.Forbidden:
                return
        if reaction.message.guild.id == 828797783863591012:
            channel = await user.create_dm()
            await channel.send('u added a  reaciton !!!!!!')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.channel.id == 782825184054476821:
            msg = after.content.split()
            dont_delete = False
            for i in msg:
                if i == '69':
                    dont_delete = True
            if not dont_delete:
                await before.delete()

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #    if member.id == 552225393571004425 and member.guild.id == 690036880812671048:
    #        await member.ban()


def setup(client):
    client.add_cog(onmsg(client))
