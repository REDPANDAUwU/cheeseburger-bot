import discord
from discord.ext import commands


class error_handling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        log_file = open('log.txt', 'a')
        log_file.write(f'Command: {ctx.command.qualified_name}, error: {error}\n')
        try:
            return await ctx.send('i broke lol!!!!')
        except:
            return


def setup(client):
    client.add_cog(error_handling(client))
