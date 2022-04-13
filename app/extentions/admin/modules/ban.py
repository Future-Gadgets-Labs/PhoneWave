from discord.ext import commands

from app.extentions.base import BaseCog
from app.utilities import logger
from app.types.discord import DiscordMessage, DiscordMember, CommandContext


class BanModule(BaseCog):
    @commands.command()
    async def ban(self, ctx: CommandContext, user: DiscordMember):
        # logger.info(f"{user} was banned")
        await ctx.send(f"{user} was banned")
