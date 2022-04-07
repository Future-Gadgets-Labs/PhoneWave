from importlib import resources
import discord.ext.commands as commands


def load_commands(client: commands.Bot):
    blacklist = ["__init__.py", "base"]
    commands = resources.contents("app.commands")
    commands = [file[:-3] for file in commands if file.endswith(".py") and file not in blacklist]

    for command in commands:
        client.load_extension(f"app.commands.{command}")


def load_event(client: commands.Bot):
    pass
