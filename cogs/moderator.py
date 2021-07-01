import discord
from discord.ext import commands
import time
import aiohttp
import json
from discord import Webhook, AsyncWebhookAdapter
import requests
import os
import re


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='gives a user all the numbers roles', hidden=True)
    @commands.has_permissions(administrator=True)
    async def numbers(self, ctx, arg: discord.Member):
        if ctx.message.guild.id != 690036880812671048:
            await ctx.message.channel.send('this is cheseburger server only comand hehe')
            return

        if ctx.message.author.guild_permissions.administrator == False:
            await ctx.message.channel.send('you cant use this command')
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
                    print('given role ' + str(role))

    @commands.command(brief='clears the channels pins',
                      description='clears the channels pins and posts them all in a seperate channel', hidden=True)
    @commands.has_permissions(administrator=True)
    async def archive(self, ctx):
        if ctx.message.guild.id != 690036880812671048:
            await ctx.message.channel.send('this is cheseburger server only comand hehe')
            return
        chnl = self.client.get_channel(742952152653365289)
        archive_channel = self.client.get_channel(742952152653365289)
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
            print(all_pins)

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
        print(ctx.message.content)

        inviter_id = arg.id

        invite_to_send = await ctx.message.channel.create_invite(max_uses=1, max_age=86400,
                                                                 reason='requested by ' + ctx.message.author.name + '#' + ctx.message.author.discriminator)
        user = self.client.get_user(int(inviter_id))
        print(user)

        await user.send('here is your instant invite ' + str(invite_to_send))
        await ctx.message.channel.send('invite sent to ' + user.name + '#' + user.discriminator)

    @invite.error
    async def invite_error(self, ctx, error):
        await ctx.send('the following error has occured, ' + str(error))

    @commands.command(hidden=True)
    async def fwtarchive(self, ctx):
        if ctx.author.id == 694482209096204308\
                or ctx.author.id == 774462774947479564\
                or ctx.author.id == 771180045917224962\
                or ctx.author.id == 822489157967806524:
            pass
        else:
            return
        if ctx.channel.guild.id == 768371462489899028:
            pass
        else:
            return
        confirmation = await ctx.send(f'archiving channel: {ctx.channel}')
        msgs = await ctx.channel.history(limit=100000).flatten()
        chnl = self.client.get_channel(801228626871844915)
        msgs.reverse()
        await confirmation.edit(content=f'archiving channel: {ctx.channel}\ndownloaded messages, deleting...')
        all_pins = await ctx.message.channel.pins()
        for i in msgs:
            try:
                if i.id != confirmation.id:
                    skip = False
                    for m in all_pins:
                        if m.id == i.id:
                            skip = True
                    if not skip:
                        if len(i.attachments) == 0:
                            # await chnl.send('from: {0}\n{1}'.format(i.author, i.content))
                            if len(str(i.content) + str(i.author)) < 2000:
                                embedz = discord.Embed(title=str(i.author), description=str(i.content), color=0x00ff00)
                                embedz.set_thumbnail(url=i.author.avatar_url)
                                embedz.set_footer(text='#' + str(ctx.channel))
                                await chnl.send(embed=embedz)
                        elif len(i.attachments) >= 1:
                            atchmnt = i.attachments[0]
                            atchmnt = atchmnt.url.split('.')
                            print(atchmnt[len(atchmnt) - 1])
                            slash = False
                            for s in re.finditer('/', atchmnt[len(atchmnt) - 1]):
                                slash = True
                            if slash:
                                atchmnt = i.attachments[0]
                                atchmnt = atchmnt.url.split('/')
                            with open('./archive/{0}.{1}'.format(i.id, atchmnt[len(atchmnt) - 1]), 'wb') as handle:
                                _json = requests.get(i.attachments[0].url, stream=True)
                                if not _json.ok:
                                    print(_json)
                                for block in _json.iter_content(1024):
                                    if not block:
                                        break
                                    handle.write(block)
                                string = './archive/{0}.{1}'.format(i.id, atchmnt[len(atchmnt) - 1])
                            if len(str(i.content) + str(i.author)) < 2000:
                                embedz = discord.Embed(title=str(i.author), description=str(i.content), color=0x00ff00)
                                embedz.set_thumbnail(url=i.author.avatar_url)
                                embedz.set_footer(text=ctx.channel)
                                pictur = self.client.get_channel(801241985171980308)
                                if os.path.getsize(string) < 8388608:
                                    imag = await pictur.send(file=discord.File(string))
                                    print(imag.attachments)
                                    embedz.set_image(url=imag.attachments[0].url)
                                await chnl.send(embed=embedz)

                        await i.delete()
            except Exception as e:
                if "NotFound" in e:
                    pass
                else:
                    ctx.send(e)
        await confirmation.edit(content='done archiving')
    
    @fwtarchive.error
    async def fwtarchive_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def dmall(self, ctx, *args):
        if ctx.guild.id != 768371462489899028 and ctx.guild.id != 825873245214343199:
            return
        if ctx.author.id != 694482209096204308 and ctx.author.id != 822489157967806524:
            return
        if len(args) == 0 and len(ctx.message.attachments) == 0:
            await ctx.send('u gotta put stuff')
            return

        success = False
        for i in await ctx.message.channel.webhooks():
            if i.channel == ctx.message.channel:
                if i.name == '_dm':
                    webhook_url = i.url
                    success = True
        if not success:
            webhook = await ctx.message.channel.create_webhook(name="_dm")
            for i in await ctx.message.channel.webhooks():
                if i.id == webhook.id:
                    webhook_url = i.url

        for m in ctx.guild.members:
            if m.id != 344817255118405632:
                # print(m)
                star = ''
                for i in args:
                    star += f' {i}'
                if len(ctx.message.attachments) > 0:
                    star += f'\n{ctx.message.attachments[0].url}'
                if m.id != self.client.user.id and not m.bot:
                    try:
                        channel = await m.create_dm()
                        await channel.send(star)
                    except discord.errors.HTTPException:
                        # await ctx.send(f"{m} has me blocked or has DM's off!")
                        requests.post(webhook_url, {'username': 'Cheeseburger Bot',
                                                    'avatar_url': str(self.client.user.avatar_url),
                                                    'content': f"<@{m.id}> has me blocked or has DM's off!"
                                                    })
        await ctx.send('done dming everyone')

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def clone(self, ctx):
        category = self.client.get_channel(710435852538478635)
        new_chnl = await ctx.message.guild.create_text_channel(ctx.message.channel.name,
                                                               category=ctx.message.channel.category,
                                                               overwrites=ctx.message.channel.overwrites)
        channel_not_made = True
        time.sleep(5)
        m = 0
        while channel_not_made:
            m += 1
            print(f"{ctx.message.channel.name}-{m}")
            if discord.utils.get(ctx.guild.channels, name=f"{ctx.message.channel.name}-{m}") is None:
                await ctx.message.channel.edit(name=f"{ctx.message.channel.name}-{m}")
                print('success')
                channel_not_made = False

        await ctx.message.channel.edit(category=category)
        role1 = discord.utils.get(ctx.message.guild.roles, name='@everyone')
        await ctx.message.channel.set_permissions(role1, read_messages=False)
        if ctx.message.guild.id == 690036880812671048:
            role2 = discord.utils.get(ctx.message.guild.roles, name='OG')
            await ctx.message.channel.set_permissions(role2, read_messages=True)

    @commands.command(hidden=True)
    async def execute(self, ctx, *args):
        star = ''
        count = 0
        for i in args:
            if count == 0:
                star += f'{i}'
                count += 1
            else:
                star += f' {i}'
        await ctx.send(exec(star))


def setup(client):
    client.add_cog(Moderator(client))
