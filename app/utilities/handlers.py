from importlib import resources
import discord.ext.commands as commands


def load_commands(client: commands.Bot):
    blacklist = ["__init__.py", "base"]
    commands = resources.contents("app.core.commands")
    commands = [file[:-3] for file in commands if file.endswith(".py") and file not in blacklist]

    for command in commands:
        client.load_extension(f"app.core.commands.{command}")


def load_events(client: commands.Bot):
    blacklist = ["__init__.py", "base"]
    events = resources.contents("app.core.events")
    events = [file[:-3] for file in events if file.endswith(".py") and file not in blacklist]

    for event in events:
        client.load_extension(f"app.core.events.{event}")
