from discord.bot import Bot as DiscordBot

import app.CLI
from app.config import Config
from app.utilities import logger
from app.types.discord import DiscordMessage


class PhoneWave(DiscordBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=self.command_prefix, **kwargs)

        self.add_cog("app.extentions.admin.AdminExtention")

    @staticmethod
    async def command_prefix(bot: "PhoneWave", message: DiscordMessage):
        return "p!"

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    def run(self):
        super().run(Config.BOT_TOKEN)
