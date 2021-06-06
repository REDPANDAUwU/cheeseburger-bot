from discord.ext import commands
import discord
import time
import os
import os.path
from git import Repo
import json
import requests


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


class pride(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='pride!!!')
    async def avatar_pride(self, ctx):
        avatar_url = ctx.author.avatar_url
        # print(avatar_url)
        atchmnt_list = str(avatar_url).split('.')
        atchmnt_end_fake = atchmnt_list[len(atchmnt_list) - 1]
        removing = False
        atchmnt_end = ''
        for i in atchmnt_end_fake:
            if i == '?':
                break
            atchmnt_end += i
        file_name = f'./content/images/flags/temp/{ctx.message.id}av.{atchmnt_end}'
        r = requests.get(avatar_url)
        with open(file_name, 'wb') as f:
            f.write(r.content)
        # with open(file_name, 'w+') as handle:
        #     print(f'{bcolors.OKBLUE}downloading image ID#{ctx.author}{bcolors.ENDC}')
        #     image = requests.get(avatar_url, stream=True)
        #     for block in image.iter_content(1024):
        #         if not block:
        #             break
        #         handle.write(str(block))
        pic = os.popen(f'convert {file_name} json:').read()
        # print(pic)
        pic = json.loads(pic)
        x = pic[0]['image']['geometry']['width']
        y = pic[0]['image']['geometry']['height']
        x += int(y/2)
        print(f'{x}:{y}')
        os.system(f'convert -geometry {x}x{y} ./content/images/flags/pedo.png ./content/images/flags/temp/'
                  f'{ctx.message.id}.png')
        os.system(f'composite -compose multiply -gravity center ./content/images/flags/temp/'
                  f'{ctx.message.id}.png {file_name} ./content/images/flags/temp/{ctx.message.id}output.png')
        await ctx.send(file=discord.File(f'./content/images/flags/temp/{ctx.message.id}output.png'))


def setup(client):
    client.add_cog(pride(client))
