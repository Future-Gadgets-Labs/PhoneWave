from discord.ext import commands
from discord.ext.commands import Context

from app.utilities import logger


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx: Context):
        logger.info("Received 'testing' command...")
        return await ctx.send("UwU")


def setup(bot):
    bot.add_cog(Ban(bot))
