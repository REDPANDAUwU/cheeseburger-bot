import json
import os
import random
import importlib

import discord
import git
from discord.ext import commands
from discord.ext import tasks

from utils import fwtarchive


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


with open("config.json") as meow:
    if json.load(meow)["debug"] == "no":
        debug = False
    else:
        debug = True

with open("version.txt") as meow:
    ver = meow.read()

with open("config.json") as meow:
    if debug:
        print(f"{bcolors.HEADER}running in debug{bcolors.ENDC}")
        prefix = json.load(meow)["debug-prefix"]
    else:
        prefix = json.load(meow)["prefix"]

bot_intents = discord.Intents.default()
bot_intents.members = True

client = commands.Bot(command_prefix=prefix, intents=bot_intents, fetch_offline_members=True, case_insensitive=True)


@client.event
async def on_ready():
    print(f'{bcolors.OKGREEN}Logged on as {client.user}!{bcolors.ENDC}')

    with open('config.json') as configf:
        config = json.load(configf)
        client.owners = config['owner-ids']
        client.fwtarchive = config['fwtarchive-channel']
        client.fwtarchivepic = config['fwtarchive-pic-channel']
        client.fwtarchiveserver = config['fwtarchive-server']
        client.autofwtarchivelist = config['fwtarchive-exclude-list']
        if debug:
            client.prefix = config['debug-prefix']
        else:
            client.prefix = config['prefix']

    if not debug:
        stunna.start()
        purge_temp.start()
        catgirl_memes.start()
        cut_carrots.start()

        client.cut_carrots = cut_carrots
        client.catgirl_memes = catgirl_memes
        auto_fwtarchive.start()
    client.debug = debug
    print(f'{bcolors.OKGREEN}loaded cheeseburger-bot version: {ver}{bcolors.ENDC}')


@client.listen('on_message')
async def on_message(message):
    print(f'{bcolors.OKCYAN}Message from {message.author}: {message.content}{bcolors.ENDC}')
    status_name = str(random.randint(0, 1000000000000000000000000000000000)) + str(
        random.randint(0, 1000000000000000000000000000000000)) + str(
        random.randint(0, 1000000000000000000000000000000000))
    await client.change_presence(activity=discord.Game(name=status_name))


@client.command(hidden=True)
async def reload(ctx):
    with open('config.json') as file:
        owners = json.load(file)["owner-ids"]
    if ctx.author.id in owners:
        if not debug:
            g = git.cmd.Git(os.getcwd())
            g.pull()
        with open('config.json') as configf:
            config = json.load(configf)
            client.owners = config['owner-ids']
            client.fwtarchive = config['fwtarchive-channel']
            client.fwtarchivepic = config['fwtarchive-pic-channel']
            client.fwtarchiveserver = config['fwtarchive-server']
            client.autofwtarchivelist = config['fwtarchive-exclude-list']

        cogs_ = os.listdir('./cogs/')
        for cog_ in cogs_:
            _cog_list = cog_.split('.')
            if _cog_list[len(_cog_list) - 1] == 'py':
                client.reload_extension(f'cogs.{_cog_list[0]}')

        importlib.reload(fwtarchive)

        await ctx.send('all cogs reloaded')


@tasks.loop(minutes=1440)
async def stunna():
    chnl = client.get_channel(823228873801465866)
    meowing = True
    stunnaboy = ''
    while meowing:
        stunnaboys = os.listdir('./content/images/Stunnaboy/')
        if len(stunnaboys) == 1:
            return
        stunnaboy = random.choice(stunnaboys)
        stunnaboy = './content/images/Stunnaboy/' + stunnaboy
        stunna_list = stunnaboy.split('.')
        if os.path.getsize(stunnaboy) < 8388608 and stunna_list[len(stunna_list) - 1] != 'md':
            meowing = False
        else:
            print(f'{bcolors.WARNING}stunnaboy too big{bcolors.ENDC}')
    await chnl.send(file=discord.File(stunnaboy))


@tasks.loop(minutes=10)
async def purge_temp():
    directory = './content/images/temp/'
    for f in os.listdir(directory):
        meow = f.split('.')
        if meow[len(meow) - 1] != "md":
            os.remove(os.path.join(directory, f))


@tasks.loop(minutes=180)
async def cut_carrots():
    # print('start carrots')
    chnl = client.get_channel(896519094042501161)
    msgs = await chnl.history(limit=100000).flatten()
    all_pins = await chnl.pins()
    for i in msgs:
        skip = False
        for m in all_pins:
            if m.id == i.id:
                skip = True
        if not skip:
            await i.delete()
    for i in sorted(os.listdir('./content/images/carrots/')):
        await chnl.send(file=discord.File(f'./content/images/carrots/{i}'))
    # print('done with carrots')


@tasks.loop(minutes=180)
async def catgirl_memes():
    # print('start catgirl memes')
    chnl = client.get_channel(896503366832762990)
    msgs = await chnl.history(limit=100000).flatten()
    all_pins = await chnl.pins()
    for i in msgs:
        skip = False
        for m in all_pins:
            if m.id == i.id:
                skip = True
        if not skip:
            await i.delete()
    for i in sorted(os.listdir('./content/images/catgirlmemes/')):
        await chnl.send(file=discord.File(f'./content/images/catgirlmemes/{i}'))
    # print('done with catgirl memes')


@tasks.loop(minutes=120)
async def auto_fwtarchive():
    # print("auto_fwtarchive")
    client.client = client
    server = client.get_guild(client.fwtarchiveserver)
    for i in server.channels:
        if "CategoryChannel" not in str(type(i)) and "VoiceChannel" not in str(type(i)) and \
                i.id not in client.autofwtarchivelist:
            await fwtarchive.fwtarchive(client, i, True)


# cogs
cogs = os.listdir('./cogs/')
for cog in cogs:
    cog_list = cog.split('.')
    if cog_list[len(cog_list) - 1] == 'py':
        client.load_extension(f'cogs.{cog_list[0]}')

with open("config.json") as meow:
    if debug:
        token = json.load(meow)["debug-token"]
    else:
        token = json.load(meow)["token"]

# client = MyClient()
client.run(token)
