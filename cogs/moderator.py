import io
import json
import os
import sys
import time

import aiohttp
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
import contextlib
import importlib

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/utils")
import fwtarchive
import dmall


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='gives a user all the numbers roles', hidden=True)
    @commands.has_permissions(administrator=True)
    async def numbers(self, ctx, arg: discord.Member):
        if ctx.message.guild.id != 690036880812671048:
            await ctx.message.channel.send('this is cheseburger server only comand hehe')
            return

        guild = ctx.message.guild
        roles = []
        await ctx.message.channel.send('giving u numbers rn')
        for i in range(70):
            # i -= 1
            for role in guild.roles:
                if role.name == str(i):
                    roles.append(role)
                    await arg.add_roles(role, reason='meow')
                    # print('given role ' + str(role))

    @commands.command(brief='clears the channels pins',
                      description='clears the channels pins and posts them all in a seperate channel', hidden=True)
    @commands.has_permissions(administrator=True)
    async def archive(self, ctx):
        if ctx.message.guild.id != 690036880812671048:
            await ctx.message.channel.send('this is cheseburger server only comand hehe')
            return
        chnl = self.client.get_channel(742952152653365289)
        # archive_channel = self.client.get_channel(742952152653365289)
        all_pins = await ctx.message.channel.pins()
        for i in all_pins:
            mat = i.attachments
            msg_link = 'https://discord.com/channels/690036880812671048/' + str(i.channel.id) + '/' + str(i.id)
            if len(mat) == 0:
                async with aiohttp.ClientSession() as session:
                    with open('config.json') as w:
                        idk = json.load(w)
                        url = idk['pinwebhookurl']
                    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(f'{discord.utils.escape_mentions(i.content)}\n{msg_link}',
                                       username=i.author.name,
                                       avatar_url=i.author.avatar_url)
                await chnl.send('‏‏‎ ‎')
            elif len(mat) == 1:
                async with aiohttp.ClientSession() as session:
                    with open('config.json') as w:
                        idk = json.load(w)
                        url = idk['pinwebhookurl']
                    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(f'{discord.utils.escape_mentions(i.content)}\n{msg_link}\n{mat[0].url}',
                                       username=i.author.name,
                                       avatar_url=i.author.avatar_url)
                await chnl.send('‏‏‎ ‎')
            else:
                async with aiohttp.ClientSession() as session:
                    with open('config.json') as w:
                        idk = json.load(w)
                        url = idk['pinwebhookurl']
                    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(f'{discord.utils.escape_mentions(i.content)}\n{msg_link}',
                                       username=i.author.name,
                                       avatar_url=i.author.avatar_url)
                    for image in range(len(mat)):
                        await webhook.send(mat[image - 1].url)
                await chnl.send('‏‏‎ ‎')
            await i.unpin(reason='to archive')
            # print(all_pins)

    @commands.command(brief='invites a user in dm with a 1 use invite', hidden=True)
    async def invite(self, ctx, arg: discord.User):
        if ctx.guild.id != 690036880812671048:
            ctx.send('dis is chezburger srvr only comands')
            return
        do_invite = False
        for i in ctx.message.author.roles:
            if i.id == 753106314510598325:
                do_invite = True
        if do_invite is not True:
            await ctx.send('u dont have invite aces')
            return
        # print(ctx.message.content)

        inviter_id = arg.id

        invite_to_send = await ctx.message.channel.create_invite(max_uses=1, max_age=86400,
                                                                 reason='requested by ' + ctx.message.author.name + '#'
                                                                        + ctx.message.author.discriminator)
        user = self.client.get_user(int(inviter_id))
        # print(user)

        await user.send('here is your instant invite ' + str(invite_to_send))
        await ctx.message.channel.send('invite sent to ' + user.name + '#' + user.discriminator)

    @invite.error
    async def invite_error(self, ctx, error):
        await ctx.send('the following error has occured, ' + str(error))

    @commands.command(hidden=True)
    async def fwtarchive(self, ctx):
        await fwtarchive.fwtarchive(self, ctx, False)

    @fwtarchive.error
    async def fwtarchive_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def dmall(self, ctx):
        await dmall.dmall(self, ctx)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def clone(self, ctx):
        if ctx.message.guild.id != 690036880812671048:
            await ctx.message.channel.send('this is cheseburger server only comand hehe')
            return
        category = self.client.get_channel(710435852538478635)
        # new_chnl = await ctx.message.guild.create_text_channel(ctx.message.channel.name,
        #                                                        category=ctx.message.channel.category,
        #                                                        overwrites=ctx.message.channel.overwrites)
        channel_not_made = True
        time.sleep(5)
        m = 0
        while channel_not_made:
            m += 1
            # print(f"{ctx.message.channel.name}-{m}")
            if discord.utils.get(ctx.guild.channels, name=f"{ctx.message.channel.name}-{m}") is None:
                await ctx.message.channel.edit(name=f"{ctx.message.channel.name}-{m}")
                # print('success')
                channel_not_made = False

        await ctx.message.channel.edit(category=category)
        role1 = discord.utils.get(ctx.message.guild.roles, name='@everyone')
        await ctx.message.channel.set_permissions(role1, read_messages=False)
        if ctx.message.guild.id == 690036880812671048:
            role2 = discord.utils.get(ctx.message.guild.roles, name='OG')
            await ctx.message.channel.set_permissions(role2, read_messages=True)

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
