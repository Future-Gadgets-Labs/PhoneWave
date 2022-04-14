"""Base setup for a module."""

from discord.ext.commands.cog import Cog
from app import PhoneWave


class BaseExtention(Cog):
    """Base Extentions, should be called if creating an extention.

    This class should only contain stuff we will reuse in all extention.

    Attributes:
        bot (PhoneWave): Instanece of the bot.
    """

    def __init__(self, bot: PhoneWave):
        self.bot = bot
