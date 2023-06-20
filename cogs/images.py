import discord
from discord.ext import commands
import random
import os
import json
import requests
from PIL import Image
import webcolors


class images(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='sends a random anime picture which is nsfw sometimes')
    async def anime(self, ctx):
        animes = os.listdir('./content/images/Nekos/')
        if len(animes) == 1:
            return
        anime = ''
        meowing = True
        while meowing:
            anime = random.choice(animes)
            anime = './content/images/Nekos/' + anime
            anime_list = anime.split('.')
            if os.path.getsize(anime) < 8388608 and anime_list[len(anime_list) - 1] != 'md':
                meowing = False
        await ctx.message.channel.send(file=discord.File(anime))

    @commands.command(brief='sends a random femboy which is nsfw sometimes')
    async def femboy(self, ctx):
        traps = os.listdir('./content/images/trap/')
        if len(traps) == 1:
            return
        trap = ''
        meowing = True
        while meowing:
            trap = random.choice(traps)
            trap = './content/images/trap/' + trap
            trap_list = trap.split('.')
            if os.path.getsize(trap) < 8388608 and trap_list[len(trap_list) - 1] != 'md':
                meowing = False
        await ctx.message.channel.send(file=discord.File(trap))

    @commands.command(brief='sends floppa')
    async def floppa(self, ctx):
        floppas = os.listdir('./content/images/floppa/')
        if len(floppas) == 1:
            return
        floppa = ''
        meowing = True
        while meowing:
            floppa = random.choice(floppas)
            floppa = './content/images/floppa/' + floppa
            floppa_list = floppa.split('.')
            if os.path.getsize(floppa) < 8388608 and floppa_list[len(floppa_list) - 1] != 'md':
                meowing = False
        await ctx.message.channel.send(file=discord.File(floppa))

    @commands.command(brief='pride!!!')
    async def avatar_pride(self, ctx):
        avatar_url = ctx.author.display_avatar
        # print(avatar_url)
        atchmnt_list = str(avatar_url).split('.')
        atchmnt_end_fake = atchmnt_list[len(atchmnt_list) - 1]
        atchmnt_end = ''
        for i in atchmnt_end_fake:
            if i == '?':
                break
            atchmnt_end += i
        file_name = f'./content/images/flags/temp/{ctx.message.id}av.{atchmnt_end}'
        r = requests.get(avatar_url)
        with open(file_name, 'wb') as f:
            f.write(r.content)
        pic = os.popen(f'convert {file_name} json:').read()
        # print(pic)
        pic = json.loads(pic)
        x = pic[0]['image']['geometry']['width']
        y = pic[0]['image']['geometry']['height']
        x += int(y / 2)
        os.system(f'convert -geometry {x}x{y} ./content/images/flags/pedo.png ./content/images/flags/temp/'
                  f'{ctx.message.id}.png')
        os.system(f'composite -compose multiply -gravity center ./content/images/flags/temp/'
                  f'{ctx.message.id}.png {file_name} ./content/images/flags/temp/{ctx.message.id}output.png')
        await ctx.send(file=discord.File(f'./content/images/flags/temp/{ctx.message.id}output.png'))

    @avatar_pride.error
    async def avatar_pride_error(self, ctx, error):
        await ctx.send(error)


async def setup(client):
    await client.add_cog(images(client))
