import discord
from discord.ext import commands
from discord.ext.commands import Context

from app.utilities import logger

ContextType = commands.Context


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        logger.info("Received 'testing' command...")
        return await ctx.send("Hello World 🥼")


def setup(bot):
    bot.add_cog(Ping(bot))
