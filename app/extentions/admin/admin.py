from app.extentions import BaseExtention
from app.extentions._base.utilities import factory

from app.utilities import logger, loaders
from app.types.discord import DiscordMessage, CommandContext


class AdminExtention(BaseExtention, name="Admin"):
    @factory.register_event()
    async def on_message(self, message: DiscordMessage):
        print("new message from " + message.author.name)

    @factory.register_command()
    async def admin(self, ctx: CommandContext):
        print("admin command called")


def setup(bot):
    parent = AdminExtention(bot)
    loaders.load_modules(bot, parent)


def teardown(bot):
    logger.info("AdminExtention teardown")
