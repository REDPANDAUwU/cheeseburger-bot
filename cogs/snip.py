import discord
from discord.ext import commands
import random
import os
import requests
import json
import aiohttp
from discord import Webhook, AsyncWebhookAdapter


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def send_to_channel(self, chnl, message, deleted):  # called on message_delete and on_message
    if message.author.bot:
        return
    msg = ''
    for i in str(message.content):
        if i == "'" or i == '"':
            i = ''
        msg += i
    user = self.client.get_user(message.author.id)
    if message.author.nick is None:
        nick1 = message.author
    else:
        nick1 = message.author.nick
    nick = ''
    for i in str(nick1):
        if i == "'" or i == '"':
            i = ''
        nick += i
    if len(message.attachments) == 0 or deleted:
        do_attachment = False
    else:
        do_attachment = True
    if not do_attachment:
        if len(message.attachments) == 0:
            await chnl.send('{"content": "' + str(msg) + '", "avatar": "' + str(
                user.avatar_url) + '", "nick": "' + str(nick) + '", "id": "' + str(message.id) + '", "image": "false"}')
        else:
            await chnl.send('{"content": "' + str(msg) + '", "avatar": "' + str(
                user.avatar_url) + '", "nick": "' + str(nick) + '", "id": "' + str(message.id) + '", "image": "true"}')
    else:
        # get server that it will use to cache images and messages
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'config.json')) as meow:
            snipe_server_id = json.load(meow)["snipe-server"]
        snipe_server = self.client.get_guild(snipe_server_id)

        # random name is to prevent multiple files being downloaded into the same directory, it isn't
        # perfect but i am lazy
        r = random.randint(1, 256)
        atchmnt = message.attachments[0].url
        atchmnt_list = atchmnt.split('.')
        atchmnt_end = atchmnt_list[len(atchmnt_list) - 1]
        snipe_channel = discord.utils.get(snipe_server.channels, name=f"{message.channel.id}-atchmnts")

        # checks if the attachment doesnt have a file ending
        if atchmnt_end.startswith('com/'):
            atchmnt_end = ''

        with open('./content/images/' + str(r) + '.' + atchmnt_end, 'wb') as handle:
            print(f'{bcolors.OKBLUE}downloading image ID#{r}{bcolors.ENDC}')
            image = requests.get(atchmnt, stream=True)
            for block in image.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        if os.path.getsize('./content/images/' + str(r) + '.' + atchmnt_end) < 8388608:
            await chnl.send(str(message.id), file=discord.File('./content/images/' + str(r) + '.' + atchmnt_end))

        os.remove('./content/images/' + str(r) + '.' + atchmnt_end)


async def snipe_script(client, message):  # called on message 'snipe' or $snipe
    if message.author.bot:
        return
    r = random.randint(1, 256)
    with open(os.path.join(os.path.dirname(__file__), os.pardir, 'config.json')) as meow:
        snipe_server_id = json.load(meow)["snipe-server"]

    snipe_server = client.get_guild(snipe_server_id)
    snipe_channel = discord.utils.get(snipe_server.channels, name=f"{message.channel.id}")
    snipe_atchmnt_channel = discord.utils.get(snipe_server.channels, name=f"{message.channel.id}-atchmnts")

    # creates a new channel if there isnt one already
    if snipe_channel is None:
        snipe_channel = await snipe_server.create_text_channel(message.channel.id)

    # get the last deleted message from the channel

    msg = await snipe_channel.history(limit=1).flatten()
    msg = msg[0]

    # writes the contents of the file to a json
    file = open(r"content/json/" + str(r) + r".json", "w+")
    file.write(msg.content)
    file.close()

    # reads the contents of the json
    with open("content/json/" + str(r) + ".json") as meow:
        content = json.load(meow)["content"]
    with open("content/json/" + str(r) + ".json") as meow:
        avatar = json.load(meow)["avatar"]
    with open("content/json/" + str(r) + ".json") as meow:
        nick = json.load(meow)["nick"]
    with open("content/json/" + str(r) + ".json") as meow:
        id = json.load(meow)["id"]
    with open("content/json/" + str(r) + ".json") as meow:
        image = json.load(meow)["image"]
    if image == 'false':
        image = False
    elif image == 'true':
        image = True
    # removes the json to save disk space
    os.remove("content/json/" + str(r) + ".json")

    do_image = False
    if snipe_atchmnt_channel is not None and image:
        number = 0
        again = True
        while again:
            number += 10
            if number > 99:
                if message.content == '':
                    await message.channel.send('cannot find a message to snipe!')
                    return
                else:
                    break
            for i in await snipe_atchmnt_channel.history(limit=number).flatten():
                try:
                    if int(i.content) == int(id):
                        do_image = True
                        atchmnt_url = i.attachments[0].url
                        again = False
                except Exception as error:
                    print(f'{bcolors.WARNING} {error}')

    success = False
    for i in await message.channel.webhooks():
        if i.channel == message.channel:
            if i.name == '_snipe':
                success = True
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(i.url, adapter=AsyncWebhookAdapter(session))
                    if do_image:
                        await webhook.send(discord.utils.escape_mentions(f"{content}\n{atchmnt_url}"),
                                           username=nick, avatar_url=avatar)
                    else:
                        await webhook.send(discord.utils.escape_mentions(content), username=nick,
                                           avatar_url=avatar)
                    success = True
    if not success:
        await message.channel.create_webhook(name="_snipe")
        for i in await message.guild.webhooks():
            if i.channel == message.channel:
                # makes sure it only uses a webhook named "_snipe"
                if i.name == '_snipe':
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(i.url, adapter=AsyncWebhookAdapter(session))
                            if do_image:
                                await webhook.send(discord.utils.escape_mentions(f"{content}\n{atchmnt_url}"),
                                                   username=nick, avatar_url=avatar)
                            else:
                                await webhook.send(discord.utils.escape_mentions(content), username=nick,
                                                   avatar_url=avatar)


class snip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.client.user:
            return

        # checking if the server is the server for caching messages
        if message.guild.id != 818293070159675444:
            snipe_server = self.client.get_guild(818293070159675444)

            # category = self.client.get_channel(818293122697396274)
            snipe_channel = discord.utils.get(snipe_server.channels, name=f"{message.channel.id}")
            # print(snipe_channel)
            if snipe_channel is None:
                new_chnl = await snipe_server.create_text_channel(name=f"{message.channel.id}")
                # print(new_chnl)
                await send_to_channel(self, new_chnl, message, True)

            else:
                await send_to_channel(self, snipe_channel, message, True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        # snipe
        if message.guild.id != 818293070159675444:
            do_cmd = True
            if len(message.attachments) == 0:
                do_cmd = False
            # if there are attachments on the message
            if do_cmd:
                # find the server and category to place the images
                snipe_server = self.client.get_guild(818293070159675444)
                category = self.client.get_channel(818311445506555935)
                snipe_channel = discord.utils.get(snipe_server.channels, name=f"{message.channel.id}-atchmnts")

                # if there isnt a channel to cache those images in yet
                if snipe_channel is None:
                    new_chnl = await snipe_server.create_text_channel(f"{message.channel.id}-atchmnts",
                                                                      category=category)
                    await send_to_channel(self, new_chnl, message, False)

                else:
                    await send_to_channel(self, snipe_channel, message, False)

        # snipes on message instead of command
        if message.content.lower() == "snipe" or message.content.lower() == "sniper":
            await snipe_script(self.client, message)
        # await self.client.process_commands(message)

    @on_message.error
    async def on_message_error(self, message, error):
        message.channel.send(f'I encountered the following error during the execution of the command!{error}')

    @commands.command(brief='sends the last deleted message')
    async def snipe(self, ctx):
        await snipe_script(self.client, ctx.message)

    @snipe.error
    async def snipe_error(self, ctx, error):
        ctx.send(f'I encountered the following error during the execution of the command!{error}')


def setup(client):
    client.add_cog(snip(client))
