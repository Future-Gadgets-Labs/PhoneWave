import discord
from discord.ext import commands

from discord.message import Message

from app.exceptions.bad_config import BadConfig
from app.database import database
from app.database.models import Guild

from app.utilities import handlers, logger
from app.config import config

prefix_cache = {}


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True  # required to fetch list of members in a guild
        intents.reactions = True  # required for 'on_raw_reaction_add' and 'on_raw_reaction_remove' events

        super().__init__(*args, intents=intents, command_prefix=self.command_prefix, **kwargs)

        # initialize the database
        database.init()

        # autoload the commands, events & the modules
        handlers.load_modules(self)

    @staticmethod
    async def command_prefix(self, message: Message):
        # this is messey but for now it does the job, later will optimize this
        prefix = prefix_cache.get(message.guild.id)
        if not prefix:
            logger.debug(f"Querying guild prefix for {message.guild.name}... & caching it")
            guild = Guild.objects(guild_id=message.guild.id).first()
            prefix = guild.prefix if guild and guild.prefix else config.BOT_PREFIX
            prefix_cache[message.guild.id] = prefix

        return prefix

    def run(self):
        if not config.BOT_TOKEN:
            raise BadConfig("BOT_TOKEN is not set.")

        super().run(config.BOT_TOKEN)
