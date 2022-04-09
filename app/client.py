from discord.ext import commands

from app.utilities import handlers


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        handlers.load_modules(self)
