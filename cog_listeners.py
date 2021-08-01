import utilities
import discord
from discord.ext import commands

class Listeners(commands.Cog, name = 'Listeners'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, ex):
        await ctx.guild.get_channel(utilities.dev_channel).send(f'<@{utilities.dev_id}> a slash command failed with the following exception: ```{ex}```')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')

def setup(bot):
    bot.add_cog(Listeners(bot))