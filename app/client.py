import discord
from discord.ext import bridge
from discord.message import Message

from app import database
from app.cache import cache_get, cache_set, check as cache_check
from app.config import config
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

        # initialize MongoDB and Redis connections
        database.init()
        cache_check()

        # autoload the commands, events & the modules
        handlers.load_modules(self)

    @staticmethod
    async def command_prefix(_bot: bridge.Bot, message: Message):
        # we need to make sure to update the cache if we update the prefix of a guild
        if message.guild is None:
            return config.BOT_PREFIX

        prefix = cache_get("prefix", guild=message.guild)
        if not prefix:
            logger.debug(f"Querying guild prefix for {message.guild.name}... & caching it")
            guild = Guild.get_guild(message.guild.id)
            prefix = guild.prefix or config.BOT_PREFIX
            cache_set("prefix", prefix, message.guild)
        return prefix

    def run(self):
        if not config.BOT_TOKEN:
            raise BadConfig("BOT_TOKEN is not set.")

        super().run(config.BOT_TOKEN)
