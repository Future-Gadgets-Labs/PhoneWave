import discord
from discord.ext import bridge
from discord.message import Message

from app.config import config
from app.cache import redis
from app.database import database
from app.database.models import Guild
from app.exceptions.bad_config import BadConfig
from app.utilities import handlers, logger


class PhoneWave(bridge.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents(
            message_content=True,
            guilds=True,
            guild_messages=True,
            guild_reactions=True,  # required to receive 'on_raw_reaction_add/remove' events
            members=True,  # required to see list of members in a guild
        )

        super().__init__(*args, intents=intents, command_prefix=self.command_prefix, **kwargs)

        # initialize the database
        database.init()

        # autoload the commands, events & the modules
        handlers.load_modules(self)

    @staticmethod
    async def command_prefix(self, message: Message):
        # we need to make sure to update the cache if we update the prefix of a guild
        if message.guild is None:
            return config.BOT_PREFIX

        if not redis.exists(id):
            logger.debug(f"Querying guild prefix for {message.guild.name}... & caching it")
            guild = Guild.objects(guild_id=message.guild.id).first()
            prefix = guild.prefix if guild and guild.prefix else config.BOT_PREFIX
            redis.set(message.guild.id, prefix)
            return prefix

        return redis.get(id)

    def run(self):
        if not config.BOT_TOKEN:
            raise BadConfig("BOT_TOKEN is not set.")

        super().run(config.BOT_TOKEN)
