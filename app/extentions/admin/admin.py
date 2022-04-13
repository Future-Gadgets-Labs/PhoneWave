from discord.ext import commands

from app.extentions.base import BaseCog
from app.utilities import logger


class AdminExtention(BaseCog):
    @BaseCog.listener()
    async def on_message(self, member):
        print("new message from " + member.name)
