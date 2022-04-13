from discord.ext.commands.cog import Cog
from discord.ext import commands


class BaseCog(Cog):
    def __init__(self, bot):
        self.bot = bot
