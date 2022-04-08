from discord.ext import commands

from app.utilities import handlers


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # autoload the commands, events & the modules
        handlers.load_package(self, "commands")
        handlers.load_package(self, "events")
        handlers.load_package(self, "modules")

        # Check for database connection
