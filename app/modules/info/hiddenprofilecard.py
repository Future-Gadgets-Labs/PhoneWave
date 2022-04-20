import discord
from discord.ext import commands
from discord.ext.commands import Context

from app.utilities import logger

ContextType = commands.Context


class Hiddenprofilecard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    #async def hiddenprofilecard(self, ctx: Context):
    async def hpc(self, ctx: Context):
        logger.info("Received 'Hiddenprofilecard' command...")
        return await ctx.send("Hiddenprofilecard hello")


def setup(bot):
    bot.add_cog(Hiddenprofilecard(bot))
