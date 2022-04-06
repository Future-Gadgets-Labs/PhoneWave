import discord
import discord.ext.commands as commands

from app.core import handlers


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # autoload the commands & the events
        handlers.load_commands(self)

    async def on_ready(self):
        print(f"Logged in as: {self.user.name} - {self.user.id}")
