import discord
import requests
import re
import os


async def fwtarchive(self, ctx, auto):
    if not auto:
        if ctx.author.id in self.client.owners:
            pass
        else:
            return
        if ctx.channel.guild.id == self.client.fwtarchiveserver:
            pass
        else:
            return
        if ctx.author.id == 497067274428219423:
            return
    confirmation = ''
    if not auto:
        confirmation = await ctx.send(f'archiving channel: {ctx.channel}')
        confirmation_id = confirmation.id
        # msgs = await ctx.channel.history(limit=100000).flatten()
        msgs = [message async for message in ctx.channel.history(limit=100000)]
    else:
        # confirmation = await ctx.send(f'archiving channel: {ctx}')
        confirmation_id = "sex"
        # msgs = await ctx.history(limit=100000).flatten()
        msgs = [message async for message in ctx.channel.history(limit=100000)]

    # gets the id of the channel stored in the config.json
    chnl = self.client.get_channel(self.client.fwtarchive)
    msgs.reverse()
    if not auto:
        await confirmation.edit(content=f'archiving channel: {ctx.channel}\ndownloaded messages, deleting...')
        all_pins = await ctx.message.channel.pins()
    else:
        # await confirmation.edit(content=f'archiving channel: {ctx}\ndownloaded messages, deleting...')
        all_pins = await ctx.pins()
    for i in msgs:
        try:
            if i.id != confirmation_id:
                skip = False
                for m in all_pins:
                    if m.id == i.id:
                        skip = True
                if not skip:
                    if len(i.attachments) == 0:
                        # await chnl.send('from: {0}\n{1}'.format(i.author, i.content))
                        if len(str(i.content) + str(i.author)) < 2000:
                            embedz = discord.Embed(title=str(i.author), description=str(i.content), color=0x00ff00)
                            embedz.set_thumbnail(url=i.author.display_avatar)
                            if not auto:
                                embedz.set_footer(text='#' + str(ctx.channel))
                            else:
                                embedz.set_footer(text='#' + str(ctx))
                            await chnl.send(embed=embedz)
                    elif len(i.attachments) >= 1:
                        atchmnt = i.attachments[0]
                        atchmnt = atchmnt.url.split('.')
                        # print(atchmnt[len(atchmnt) - 1])
                        slash = False
                        for _ in re.finditer('/', atchmnt[len(atchmnt) - 1]):
                            slash = True
                        if slash:
                            atchmnt = i.attachments[0]
                            atchmnt = atchmnt.url.split('/')
                        with open('./archive/{0}.{1}'.format(i.id, atchmnt[len(atchmnt) - 1]), 'wb') as handle:
                            _json = requests.get(i.attachments[0].url, stream=True)
                            if not _json.ok:
                                print(_json)
                            for block in _json.iter_content(1024):
                                if not block:
                                    break
                                handle.write(block)
                            string = './archive/{0}.{1}'.format(i.id, atchmnt[len(atchmnt) - 1])
                        if len(str(i.content) + str(i.author)) < 2000:
                            embedz = discord.Embed(title=str(i.author), description=str(i.content), color=0x00ff00)
                            embedz.set_thumbnail(url=i.author.display_avatar)
                            if not auto:
                                embedz.set_footer(text=ctx.channel)
                            else:
                                embedz.set_footer(text=ctx)
                            pictur = self.client.get_channel(self.client.fwtarchivepic)
                            if os.path.getsize(string) < 8388608:
                                imag = await pictur.send(file=discord.File(string))
                                # print(imag.attachments)
                                embedz.set_image(url=imag.attachments[0].url)
                            await chnl.send(embed=embedz)
                        os.remove('./archive/{0}.{1}'.format(i.id, atchmnt[len(atchmnt) - 1]))

                    await i.delete()
        except Exception as e:
            if "NotFound" in e:
                pass
            else:
                ctx.send(f'warn: {e}')
    if not auto:
        await ctx.send('done archiving')

