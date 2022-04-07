import discord
from discord.ext import commands

from app.utilities import handlers


async def on_ready():
    print("ready")


async def uwu(ctx):
    print("working")


class PhoneWave(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # autoload the commands & the events
        handlers.load_commands(self)

        self.event(on_ready)
        
        result = commands.command()(uwu)
        self.add_command(result)
        

    # async def on_ready(self):
    #     print(f"Logged in as: {self.user.name} - {self.user.id}")
