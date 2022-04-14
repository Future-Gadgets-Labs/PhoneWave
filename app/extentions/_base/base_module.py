"""Base setup for a module."""

from discord.ext.commands.cog import Cog
from app import PhoneWave


class BaseModule(Cog):
    """Base Module, should be called if creating a module.

    This class should only contain stuff we will reuse in all extention.

    Attributes:
        bot (PhoneWave): Instanece of the bot.
        parent (Extention): Parent of the module, usally its the extention.

    Note:
        if "name" metaclass attribute is not set, the module will have the same name as the parent.
    """

    def __init__(self, bot: PhoneWave, parent):
        self.bot = bot
        self.parent = parent

        # The module should have the same name as the parent
        # unless specified otherwise.

        if self.__class__.__name__ == self.qualified_name:
            self.__cog_name__ = self.parent.__cog_name__
