from discord.ext import commands

from app.database import database
from app.utilities import handlers


class PhoneWave(commands.Bot):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, command_prefix=config.get("bot_prefix"), **kwargs)

        self.config = config

        # autoload the commands, events & the modules
        handlers.load_modules(self)

        # initialize the database
        self.db_client = database.get_client(self.config)
        self.db = self.db_client[config.get("mongo_database")]

    def run(self):
        token = self.config.get("bot_token")
        super().run(token)
