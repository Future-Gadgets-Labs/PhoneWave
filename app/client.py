from discord.ext import commands

from app.utilities import handlers


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # autoload the commands, events & the modules
        handlers.load_commands(self)
        handlers.load_events(self)
        handlers.load_modules(self)

        # Check for database connection
