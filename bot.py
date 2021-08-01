import utilities
import discord
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix=utilities.prefix)
slash = SlashCommand(bot, override_type = True, sync_commands=True)
bot.load_extension("cog_verify")
bot.load_extension("cog_listeners")
bot.run(utilities.token)