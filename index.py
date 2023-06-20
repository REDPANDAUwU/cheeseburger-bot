import json
import os
import random
import importlib
import datetime

import discord
from discord.ext import commands
from discord.ext import tasks

from utils import fwtarchive
from utils import langgen


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
    debug = False

with open("config.json") as meow:
    prefix = json.load(meow)["prefix"]

bot_intents = discord.Intents.default()
bot_intents.members = True
bot_intents.message_content = True

client = commands.Bot(command_prefix=prefix, intents=bot_intents, fetch_offline_members=True, case_insensitive=True)


@client.event
async def on_ready():
    # cogs
    cogs = os.listdir('./cogs/')
    for cog in cogs:
        cog_list = cog.split('.')
        if cog_list[len(cog_list) - 1] == 'py':
            # print(cog)
            await client.load_extension(f'cogs.{cog_list[0]}')
    # await client.load_extension('cogs.misc')

    print(f'{bcolors.OKGREEN}Logged on as {client.user}!{bcolors.ENDC}')

    with open('config.json') as configf:
        config = json.load(configf)
        client.owners = config['owner-ids']
        client.fwtarchive = config['fwtarchive-channel']
        client.fwtarchivepic = config['fwtarchive-pic-channel']
        client.fwtarchiveserver = config['fwtarchive-server']
        client.autofwtarchivelist = config['fwtarchive-exclude-list']
        client.prefix = config['prefix']

    purge_temp.start()
    catgirl_memes.start()
    cut_carrots.start()

    client.cut_carrots = cut_carrots
    client.catgirl_memes = catgirl_memes
    auto_fwtarchive.start()

    client.debug = False
    client.write_queue = []
    print(f'{bcolors.OKGREEN}loaded cheeseburger-bot{bcolors.ENDC}')


@client.listen('on_message')
async def on_message(message):
    if message.content.strip() != '':
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
                await client.reload_extension(f'cogs.{_cog_list[0]}')

        importlib.reload(fwtarchive)

        await ctx.send('all cogs reloaded')

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
    # msgs = await chnl.history(limit=100000).flatten()
    msgs = [message async for message in chnl.history(limit=100000)]
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
    try:
        chnl = client.get_channel(896503366832762990)
        # msgs = await chnl.history(limit=100000).flatten()
        msgs = [message async for message in chnl.history(limit=100000)]
        all_pins = await chnl.pins()
        for i in msgs:
            # skip = False
            # for m in all_pins:
            #     if m.id == i.id:
            #         skip = True
            # if not skip:
            #     await i.delete()  what the fuck was i thinking when i wrote this
            if i not in all_pins:
                await i.delete()
        for i in sorted(os.listdir('./content/images/catgirlmemes/')):
            await chnl.send(file=discord.File(f'./content/images/catgirlmemes/{i}'))
    except Exception as e:
        log_file = open('log.txt', 'a')
        log_file.write(f'Command: catgirlmemes, error: {e}, {datetime.datetime.now()}\n')
        log_file.close()

    # print('done with catgirl memes')


@tasks.loop(minutes=120)
async def auto_fwtarchive():
    try:
        # print("auto_fwtarchive")
        client.client = client
        server = client.get_guild(client.fwtarchiveserver)
        for i in server.channels:
            if "CategoryChannel" not in str(type(i)) and "VoiceChannel" not in str(type(i)) and \
                    i.id not in client.autofwtarchivelist:
                await fwtarchive.fwtarchive(client, i)
    except Exception as e:
        log_file = open('log.txt', 'a')
        log_file.write(f'Command: fwtarchive, error: {e}, {datetime.datetime.now()}\n')
        log_file.close()
        print(f'Command: fwtarchive, error: {e}, {datetime.datetime.now()}\n')


with open("config.json") as meow:
    token = json.load(meow)["token"]

# client = MyClient()
client.run(token)
