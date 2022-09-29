import json
import os
import random
import importlib
import datetime
import requests

import discord
import git
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
        make_steam_dick.start()
    else:
        # client.steam_dick_data = open('data.bich', 'r').read().split('\n')
        # make_steam_dick.start()
        client.steam_dick_data = open('content/data.bich', 'r').read().replace('\t', ' ').split('\n')
    regen_datatable.start()
    client.debug = debug
    client.write_queue = []
    print(f'{bcolors.OKGREEN}loaded cheeseburger-bot version: {ver}{bcolors.ENDC}')
    # channel = client.get_channel(879058785656791080)
    # print('collecting messages...')
    # message = await channel.history(limit=50000).flatten()
    # print('adding to log file')
    # for i in message:
    #     # print(i.embeds[0].title)\
    #     try:
    #         if i.embeds[0].title != "Cheeseburger Bot#7278" and i.embeds[0].description.strip() != '' \
    #                 and i.embeds[0].title.split('#')[1] != '0000':
    #             log_file = open('log_fwt.txt', 'a')
    #             log_file.write(f'{i.embeds[0].description}\n')
    #             log_file.close()
    #     except:
    #         pass
    # print('done!!!!')


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
        if not debug:
            g = git.cmd.Git(os.getcwd())
            g.pull()
            regen_datatable.restart()
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
                await fwtarchive.fwtarchive(client, i, True)
    except Exception as e:
        log_file = open('log.txt', 'a')
        log_file.write(f'Command: fwtarchive, error: {e}, {datetime.datetime.now()}\n')
        log_file.close()


@tasks.loop(minutes=5)
async def regen_datatable():
    text = open('./input.txt').read()

    text_list = text.split('\n')

    # rebuild text_list
    new_text_list = []
    for i in text_list:
        if i.strip() != '' and i.strip('\n') != '':
            new_text_list.append(i.strip())
    text_list = new_text_list

    datatable = langgen.generate_datatable(text_list)

    client.lang_gen_datatable = datatable


@tasks.loop(minutes=120)
async def make_steam_dick():
    r = requests.get("https://docs.google.com/spreadsheets/d/1ngfg2eP8E_Ue81lqGl6v34uVJ73qrfnq9S-H1aCZGD0/"
                     "export?format=tsv&gid=277245429")
    with open('content/data.bich', 'wb') as f:
        f.write(r.content)
    client.steam_dick_data = open('content/data.bich', 'r').read().split('\n')


with open("config.json") as meow:
    if debug:
        token = json.load(meow)["debug-token"]
    else:
        token = json.load(meow)["token"]

# client = MyClient()
client.run(token)
