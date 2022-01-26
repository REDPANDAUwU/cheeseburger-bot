import discord
import requests


async def dmall(self, ctx, args, on_msg=False):
    # if ctx.guild.id != 768371462489899028 and ctx.guild.id != 825873245214343199:
    #    return
    # if ctx.author.id != 694482209096204308 and ctx.author.id != 822489157967806524:
    #    return

    # this prevents the function getting ran twice from 1 message
    if not on_msg:
        if ctx.author.id == 656962312565030963:
            return
    # print(args)
    if len(args) == 0 and len(ctx.attachments) == 0:
        await ctx.channel.send('u gotta put stuff')
        return
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

    for m in ctx.guild.members:
        if m.id != 344817255118405632:
            # print(m)
            star = ''

            for i in args:
                star += f' {i}'
            if len(ctx.attachments) > 0:
                star += f'\n{ctx.attachments[0].url}'
            star += f'\n- sent by {ctx.author}'
            if m.id != self.client.user.id and not m.bot:
                try:
                    channel = await m.create_dm()
                    await channel.send(f'<@{m.id}>{star}')
                except discord.errors.HTTPException:
                    # await ctx.send(f"{m} has me blocked or has DM's off!")
                    sent = False
                    while not sent:
                        callback = requests.post(webhook_url, {'username': 'Cheeseburger Bot',
                                                               'avatar_url': str(self.client.user.avatar_url),
                                                               'content': f"<@{m.id}> has me blocked or has DM's off!"
                                                               })
                        if '204' in str(callback):
                            # print('success')
                            sent = True
                        # else:
                        #     print('loop')

    await ctx.channel.send('done dming everyone')
