from app.extentions._base.utilities import factory
from app.extentions._base import BaseModule
from app.utilities import logger
from app.types.discord import DiscordMessage, CommandContext, DiscordMember


class PurgeModule(BaseModule):
    @factory.register_command()
    async def purge(self, ctx: CommandContext, user: DiscordMember):
        await ctx.send(f"{user} was purged")


__CLASS = PurgeModule
