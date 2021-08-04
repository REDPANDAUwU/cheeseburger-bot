import discord
from discord.ext import commands
from discord.ext import tasks
import os
import json
import random
import git


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

    if not debug:
        stunna.start()
        purge_temp.start()
        catgirl_memes.start()
        cut_carrots.start()
        client.cut_carrots = cut_carrots
        client.catgirl_memes = catgirl_memes
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
        owner = json.load(file)["owner-id"]
    if ctx.author.id == owner:
        if not debug:
            g = git.cmd.Git(os.getcwd())
            g.pull()

        cogs = os.listdir('./cogs/')
        for cog in cogs:
            cog_list = cog.split('.')
            if cog_list[len(cog_list) - 1] == 'py':
                client.reload_extension(f'cogs.{cog_list[0]}')

        await ctx.send('all cogs reloaded')


@tasks.loop(minutes=1440)
async def stunna():
    chnl = client.get_channel(823228873801465866)
    meowing = True
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
    dir = './content/images/temp/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


@tasks.loop(minutes=5)
async def catgirl_memes():
    channel = client.get_channel(846013796983373845)
    if channel.name != 'no-catgirl-memes':
        await channel.edit(name='no-catgirl-memes', topic='Channel solely for catgirl nbot allowing catgrilmemes')


@tasks.loop(minutes=360)
async def cut_carrots():
    print('start carrots')
    chnl = client.get_channel(859239242143367198)
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
    print('done with carrots')


@tasks.loop(minutes=360)
async def catgirl_memes():
    print('start catgirl memes')
    chnl = client.get_channel(846013796983373845)
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
    print('done with catgirl memes')


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
