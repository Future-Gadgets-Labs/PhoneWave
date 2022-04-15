from discord.ext.commands.bot import Bot as DiscordBot

import app.CLI
from app.config import Config
from app.utilities import logger, loaders, SingletonMeta
from app.types.discord import DiscordMessage


class PhoneWave(DiscordBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=self.command_prefix, **kwargs)
        loaders.load_extentions(self)

    @staticmethod
    async def command_prefix(bot: "PhoneWave", message: DiscordMessage):
        return "p!"

    async def on_message(self, message: DiscordMessage):
        if message.author.id == self.user.id:
            return

        await self.process_commands(message)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    def run(self):
        super().run(Config.BOT_TOKEN)
