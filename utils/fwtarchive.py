import discord
import requests
import re
import os


async def fwtarchive(self, channel, auto=True):
    all_pins = await channel.pins()
    confirmation = None  # there u go are u happy now pycharm now u wont fucking highlight line 21
    if not auto:
        confirmation = await channel.send(f'archiving channel: {channel}')
        # confirmation_id = confirmation.id
        all_pins.append(confirmation)  # this is a hacky way to make the bot not delete the confirmation message
    msgs = [message async for message in channel.history(limit=100000)]

    # gets the id of the channel stored in the config.json
    chnl = self.client.get_channel(self.client.fwtarchive)
    msgs.reverse()
    if not auto:
        await confirmation.edit(content=f'archiving channel: {channel}\ndownloaded messages, deleting...')

    # print(msgs)
    for i in msgs:
        try:
            if i not in all_pins:
                if len(i.attachments) == 0:
                    # await chnl.send('from: {0}\n{1}'.format(i.author, i.content))
                    if len(str(i.content) + str(i.author)) < 2000:
                        embedz = discord.Embed(title=str(i.author), description=str(i.content), color=0x00ff00)
                        embedz.set_thumbnail(url=i.author.display_avatar)
                        embedz.set_footer(text='#' + str(channel))
                        await chnl.send(embed=embedz)
                else:
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
                        embedz.set_footer(text=channel)
                        pictur = self.client.get_channel(self.client.fwtarchivepic)
                        if os.path.getsize(string) < 8388608:  # if the attachment is > 8 mb
                            imag = await pictur.send(file=discord.File(string))
                            # print(imag.attachments)
                            embedz.set_image(url=imag.attachments[0].url)
                        await chnl.send(embed=embedz)
                    os.remove('./archive/{0}.{1}'.format(i.id, atchmnt[len(atchmnt) - 1]))

                await i.delete()
        except discord.NotFound:
            pass  # this means that the message was deleted in the middle of archiving
    if not auto:
        await channel.send('done archiving')

