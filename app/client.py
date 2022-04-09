from discord.ext import commands

from discord.message import Message

from app.exceptions.bad_config import BadConfig
from app.database import database
from app.database.models import Guild

from app.utilities import handlers, logger
from app.config import config

temp_cache = {}


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=self.command_prefix, **kwargs)

        # autoload the commands, events & the modules
        handlers.load_modules(self)

        # initialize the database
        database.init()

    @staticmethod
    async def command_prefix(self, message: Message):
        # this is messey but for now it does the job, later will optimize this
        if message.guild.id in temp_cache:
            return temp_cache[message.guild.id]
        else:
            logger.debug(f"Quierying guild prefix for {message.guild.name}... & caching it")
            guild = Guild.objects(gid=message.guild.id).first()
            temp_cache[message.guild.id] = guild.prefix if guild else config.BOT_PREFIX

            if not guild:
                Guild(gid=message.guild.id, prefix=config.BOT_PREFIX).save()

            return temp_cache[message.guild.id]

    def run(self):
        if not config.BOT_TOKEN:
            raise BadConfig("BOT_TOKEN is not set.")

        super().run(config.BOT_TOKEN)
