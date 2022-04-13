from discord.ext import commands

from ..admin import AdminExtention
from app.utilities import logger


class BanModule(AdminExtention):
    #

    @AdminExtention.listener()
    async def on_message(self, member):
        print("new message from " + member.name)
