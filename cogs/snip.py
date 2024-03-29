import discord
from discord.ext import commands
import os
import requests
import json
import urllib.request


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


async def save_images(client, message):
    do_cmd = True
    if len(message.attachments) == 0:
        do_cmd = False
    archiv_img_url = "meow"
    # if there are attachments on the message
    if do_cmd:
        # find the server and category to place the images
        archiv_img_url = await send_to_channel(message, client)

    # removes all quotes from the message, so the json interpreter doesnt mess up
    msg = ''
    for i in str(message.content):
        if i == "'" or i == '"':
            i = ''
        msg += i

    # uses the users nickname if the user has one for that guild

    try:
        if message.author.nick is None:
            nick1 = message.author
        else:
            nick1 = message.author.nick
    except AttributeError:
        nick1 = message.author

    # if message.author.guild_avatar is None:
    #     avatar = message.author.avatar_url
    # else:
    #     avatar = message.author.guild_avatar
    avatar = message.author.display_avatar

    nick = ''
    # removes all quotes from the name, so the json interpreter doesnt mess up
    for i in str(nick1):
        if i == "'" or i == '"':
            i = ''
        nick += i
    # writing contents of the message to a json
    with open("content/json/msg/" + str(message.id) + ".json", "w+") as meow:
        if len(message.attachments) == 0:
            meow.write('{"content": "' + str(msg) + '", "avatar": "' + str(
                avatar) + '", "nick": "' + str(nick) + '", "id": "' + str(
                message.id) + '", "image": "false"}')
        # tells the bot whether the message had a image in it
        else:
            meow.write('{"content": "' + str(msg) + '", "avatar": "' + str(
                avatar) + '", "nick": "' + str(nick) + '", "id": "' + str(
                message.id) + '", "image": "' + str(archiv_img_url) + '"}')
        meow.close()


async def send_to_channel(message, client):  # called on message_delete and on_message
    if message.author.bot:
        return

    with open(os.path.join(os.path.dirname(__file__), os.pardir, 'config.json')) as meow:
        snipe_channel_id = json.load(meow)["snipe-channel"]

    atchmnt = message.attachments[0].url
    blahblah = message.attachments[0].url
    atchmnt = atchmnt.split("?")[0]  # discord added new tracking things at the end of a link for some reason
    atchmnt_list = atchmnt.split('.')
    atchmnt_end = atchmnt_list[len(atchmnt_list) - 1]
    snipe_channel = client.get_channel(snipe_channel_id)

    # checks if the attachment doesnt have a file ending
    if atchmnt_end.startswith('com/'):
        atchmnt_end = ''

    print(f'{bcolors.OKBLUE}downloading image ID#{message.id}{bcolors.ENDC}')
    req = urllib.request.Request(blahblah, headers={'User-Agent': 'Mozilla/5.0'})
    with open('./content/images/' + str(message.id) + '.' + atchmnt_end, 'wb') as f:
        with urllib.request.urlopen(req) as r:
            f.write(r.read())

    if os.path.getsize('./content/images/' + str(message.id) + '.' + atchmnt_end) < 8388608:
        aa = await snipe_channel.send(str(message.id), file=discord.File('./content/images/' + str(message.id) + '.' +
                                                                         atchmnt_end))
        os.remove('./content/images/' + str(message.id) + '.' + atchmnt_end)
        return aa.attachments[0].url.split("?")[0]

    os.remove('./content/images/' + str(message.id) + '.' + atchmnt_end)


async def snipe_script(client, message):  # called on message 'snipe' or $snipe
    # print('snipe script')
    if message.author.bot:
        # print('return')
        return

    with open("content/json/" + str(message.channel.id) + ".json", "r") as meow:
        meowmeow = json.load(meow)
        msg_id = meowmeow["meow"]
        image = meowmeow["imag"]

    # reads the contents of the message id json
    with open("content/json/msg/" + str(msg_id) + ".json", "r") as meow:
        meowmeow = json.load(meow)
        # print(meowmeow)
        content = meowmeow["content"]
        avatar = meowmeow["avatar"]
        nick = meowmeow["nick"]
        atchmnt = meowmeow["image"]

    if image == 'false':
        atchmnt_url = "meow"
        image = False
    else:
        atchmnt_url = atchmnt
        image = True
    if client.debug:
        webhook_name = '_testsnipe'
    else:
        webhook_name = '_snipe'
    success = False
    for i in await message.channel.webhooks():
        if i.name == webhook_name:
            # print(i)
            if image:
                webhook = {"username": nick, "avatar_url": avatar,
                           "content": f"{discord.utils.escape_mentions(content)}\n{atchmnt_url}"}
            else:
                webhook = {"username": nick, "avatar_url": avatar,
                           "content": f"{discord.utils.escape_mentions(content)}"}
            requests.post(i.url, json.dumps(webhook), headers={"Content-Type": "application/json"})
            # print(i.url)
            # print(json.dumps(webhook))
            success = True
    if not success:
        i = await message.channel.create_webhook(name=webhook_name)
        # makes sure it only uses a webhook named "_snipe"
        if i.name == webhook_name:
            if image:
                webhook = {"username": nick, "avatar_url": avatar,
                           "content": f"{discord.utils.escape_mentions(content)}\n{atchmnt_url}"}
            else:
                webhook = {"username": nick, "avatar_url": avatar,
                           "content": f"{discord.utils.escape_mentions(content)}"}

            requests.post(i.url, json.dumps(webhook), headers={"Content-Type": "application/json"})
    # print('end of snipe script')


class snip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.client.user or message.author.bot:
            return

        msg = ''
        for i in str(message.content):
            if i == "'" or i == '"':
                i = ''
            msg += i
        nick1 = message.author.display_name
        nick = ''
        for i in str(nick1):
            if i == "'" or i == '"':
                i = ''
            nick += i

        with open("content/json/" + str(message.channel.id) + ".json", "w+") as meow:
            if len(message.attachments) == 0:
                meow.write('{"meow": "' + str(message.id) + '", "imag": "false"}')
            else:
                meow.write('{"meow": "' + str(message.id) + '", "imag": "true"}')
            meow.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        # save all images to a channel
        await save_images(self.client, message)

        # snipes on message instead of command
        if message.content.lower() == 'snipe' or message.content.lower() == 'sniper' \
                or message.content.lower() == 'thnipe':
            await snipe_script(self.client, message)
        # await self.client.process_commands(message)

    @commands.command(brief='sends the last deleted message')
    async def snipe(self, ctx):
        await snipe_script(self.client, ctx.message)


async def setup(client):
    await client.add_cog(snip(client))
