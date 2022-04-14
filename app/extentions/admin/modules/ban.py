from discord.ext import commands

from app.extentions._base import BaseModule
from app.utilities import logger
from app.types.discord import DiscordMessage, DiscordMember, CommandContext


class BanModule(BaseModule):
    @commands.command()
    async def ban(self, ctx: CommandContext, user: DiscordMember):
        # logger.info(f"{user} was banned")
        await ctx.send(f"{user} was banned")


__CLASS = BanModule
