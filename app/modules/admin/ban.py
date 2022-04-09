from discord.ext import commands

from app.utilities import logger

ContextType = commands.Context


class BotCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx: ContextType):
        logger.info("Received 'testing' command...")
        return await ctx.send("UwU")


def setup(bot):
    bot.add_cog(BotCommand(bot))