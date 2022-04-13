from discord.ext import commands

from app.extentions.base import BaseCog
from app.utilities import logger


class AdminExtention(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @BaseCog.listener()
    async def on_message(self, member):
        print("new message from " + member.name)
