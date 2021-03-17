from typing import TextIO
import discord
from discord import NotFound
import time
from discord.ext import commands
from discord.ext import tasks
from discord import Webhook, AsyncWebhookAdapter
from discord.ext.commands import has_permissions
from discord.ext.commands.errors import MissingPermissions
from discord.utils import get
import asyncio
import os
import json
import random
import requests
import re
from gtts import gTTS
import time
import sqlite3
import aiohttp
import logging
import git
from git import repo, Repo


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
    print(f'{bcolors.OKGREEN}loaded cheeseburger-bot version: {ver}{bcolors.ENDC}')
    if not debug:
        stunna.start()


@client.listen('on_message')
async def on_message(message):
    print(f'{bcolors.OKCYAN}Message from {message.author}: {message.content}{bcolors.ENDC}')
    status_name = str(random.randint(0, 1000000000000000000000000000000000)) + str(
        random.randint(0, 1000000000000000000000000000000000)) + str(
        random.randint(0, 1000000000000000000000000000000000))
    await client.change_presence(activity=discord.Game(name=status_name))


@tasks.loop(minutes=1440)
async def stunna():
    chnl = client.get_channel(820837463961501706)
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


@client.command(hidden=True)
async def reload(ctx):
    with open('config.json') as meow:
        owner = json.load(meow)["owner-id"]
    if ctx.author.id == owner:
        g = git.cmd.Git(os.getcwd())
        g.pull()

        client.reload_extension('cogs.info')

        client.reload_extension('cogs.moderator')

        client.reload_extension('cogs.images')

        client.reload_extension('cogs.misc')

        client.reload_extension('cogs.snip')

        client.reload_extension('cogs.onmsg')

        await ctx.send('all cogs reloaded')


# cogs


client.load_extension('cogs.info')

client.load_extension('cogs.moderator')

client.load_extension('cogs.images')

client.load_extension('cogs.misc')

client.load_extension('cogs.snip')

client.load_extension('cogs.onmsg')

with open("config.json") as meow:
    if debug:
        token = json.load(meow)["debug-token"]
    else:
        token = json.load(meow)["token"]

# client = MyClient()
client.run(token)
