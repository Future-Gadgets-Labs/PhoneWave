from discord.ext import commands

from app.utilities import logger


class ClientEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.bot.user}")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        logger.error(f"{event}")


def setup(bot):
    bot.add_cog(ClientEvents(bot))
