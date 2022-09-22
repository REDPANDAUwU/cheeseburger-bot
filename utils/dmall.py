import discord
import requests
import time
import asyncio


async def webhook_ping(webhook, av_url, user):
    sent = False
    while not sent:
        callback = requests.post(webhook, {'username': 'Cheeseburger Bot',
                                           'avatar_url': str(av_url),
                                           'content': f"<@{user}> has me blocked or has DM's off!"
                                           })
        if '204' in str(callback):
            # print('success')
            sent = True

        time.sleep(.5)
    # print('thready is done!!!!')


async def dmall(self, ctx, on_msg=False):
    # if ctx.guild.id != 768371462489899028 and ctx.guild.id != 825873245214343199:
    #    return
    # if ctx.author.id != 694482209096204308 and ctx.author.id != 822489157967806524:
    #    return
    # print('emwo')
    # print(ctx.message.content)

    # print('emo2')
    # this prevents the function getting ran twice from 1 message
    if not on_msg:
        if ctx.author.id == 656962312565030963 or ctx.author.id == 694482209096204308:
            print('eopic')
            return
    # print(args)
    try:
        if ctx.message.content.split()[1] == "--raw":
            cutoff = 13
            raw = True
        else:
            raw = False
            cutoff = 7
    except IndexError:
        raw = False
        cutoff = 7

    if len(ctx.message.content[cutoff:].strip()) == 0 and len(ctx.message.attachments) == 0:
        await ctx.channel.send('u gotta put stuff')
        return
    ctx.message.content = ctx.message.content[cutoff:]

    # check if user wants to send a raw message (no ping/author text)
    # try:
    #     if ctx.message.content.split()[1] == "--raw":
    #         raw = True
    #         ctx.message.content = ctx.message.content[13:]
    #     else:
    #         raw = False
    # except IndexError:
    #     raw = False

    webhook_url = ''
    success = False
    for i in await ctx.channel.webhooks():
        if i.channel == ctx.channel:
            if i.name == '_dm':
                webhook_url = i.url
                success = True
    if not success:
        webhook = await ctx.channel.create_webhook(name="_dm")
        for i in await ctx.channel.webhooks():
            if i.id == webhook.id:
                webhook_url = i.url
    #     threads = []
    for m in ctx.guild.members:
        if m.id != 344817255118405632:
            # print(m)
            star = ctx.message.content

            # for i in args:
            #     star += f' {i}'
            if len(ctx.message.attachments) > 0:
                star += f'\n{ctx.message.attachments[0].url}'
            if not raw:
                star += f'\n- sent by {ctx.author}'
            star = f"<@{m.id}> {star}"
            if m.id != self.client.user.id and not m.bot:
                try:
                    channel = await m.create_dm()
                    await channel.send(f'{star}')
                except discord.errors.HTTPException:
                    requests.post(webhook_url, {'username': 'Cheeseburger Bot',
                                                'avatar_url': str(self.client.user.avatar),
                                                'content': f"<@{m.id}> has me blocked or has DM's off!"
                                                })

    #                     new_thread = threading.Thread(target=webhook_ping, args=(webhook_url,
    #                                                                              self.client.user.avatar_url,
    #                                                                              m.id))
    #                     new_thread.start()
    #                     threads.append(new_thread)
    # print('thread started')

    await ctx.channel.send('done dming everyone')
