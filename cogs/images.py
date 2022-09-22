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

    @commands.command(hidden=True)
    async def myballsitch(self, ctx):
        if ctx.message.guild.id != 690036880812671048:
            await ctx.message.channel.send('this is cheseburger server only comand hehe')
            return
        if ctx.message.channel == self.client.get_channel(763928465908826182):
            for i in range(10):
                await ctx.message.channel.send(file=discord.File('./content/images/myballsitch.png'))
        elif ctx.message.channel != self.client.get_channel(763928465908826182):
            await ctx.message.channel.send('wrong channel use <#763928465908826182>')

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

    @commands.command()
    async def dumpy(self, ctx):
        if True:  # len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0].url
            file_name_fake = attachment.split('.')
            file_name_end = file_name_fake[len(file_name_fake) - 1]
            file_name = f'./content/images/temp/{ctx.message.id}.{file_name_end}'
            # file_name = './content/images/temp/851672722543214593.png'
            r = requests.get(attachment)
            with open(file_name, 'wb') as f:
                f.write(r.content)
            output_file_name = f"./content/images/temp/{ctx.message.id}output.png"
            # output_file_name = './content/images/temp/851672722543214593output.png'
            os.system(f'convert -resize 10x10 {file_name} {output_file_name}')
            # await ctx.send(file=discord.File(output_file_name))
            among_us_files = "./content/images/dumpy/gifs/"
            # get data of image input
            picture = Image.open(output_file_name, 'r')
            pixels = picture.load()
            grid = []
            for x in range(10):
                column = []
                for y in range(10):
                    try:
                        # print('emow')
                        r, g, b, a = pixels[x, y]
                        r -= r % 10
                        g -= g % 10
                        b -= b % 10
                        rgb = (r, g, b)
                        # print(rgb)

                        column.append(webcolors.rgb_to_hex(rgb))
                    except IndexError:
                        pass
                grid.append(column)

            picture.close()

            # what needs to be done: make a for loop for each pixel in the 50x50 image
            strang = ''
            for i in grid:
                for n in i:
                    strang += f'{among_us_files}{n.strip("#")}.gif '
            await ctx.send('creating your gif!')
            os.system(f'convert {strang} -adjoin -geometry 400x400 ./content/images/temp/{ctx.message.id}complete.gif')
            # os.system(f'convert ./content/images/temp/{ctx.message.id}almost.gif -resize 400x400 '
            #           f'./content/images/temp/{ctx.message.id}complete.gif')
            await ctx.send(file=discord.File(f'./content/images/temp/{ctx.message.id}complete.gif'))


async def setup(client):
    await client.add_cog(images(client))
