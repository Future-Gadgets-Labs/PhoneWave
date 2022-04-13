from discord.ext import commands

from app.extentions.base import BaseCog
from app.utilities import logger
from app.types.discord import DiscordMessage

from .modules import BanModule


class AdminExtention(BaseCog):
    @BaseCog.listener()
    async def on_message(self, message: DiscordMessage):
        print("new message from " + message.author.name)


def setup(bot):
    bot.add_cog(AdminExtention(bot))
    bot.add_cog(BanModule(bot))


def teardown(bot):
    logger.info("AdminExtention teardown")
