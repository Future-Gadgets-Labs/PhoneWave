import discord
from discord.ext import bridge
from discord.message import Message

from app.config import config
from app.database import database
from app.database.models import Guild
from app.exceptions.bad_config import BadConfig
from app.utilities import handlers, logger

prefix_cache = {}


class PhoneWave(bridge.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents(
            message_content=True,
            guilds=True,
            guild_messages=True,
            guild_reactions=True,  # required to receive 'on_raw_reaction_add/remove' events
            members=True,          # required to see list of members in a guild
        )

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
