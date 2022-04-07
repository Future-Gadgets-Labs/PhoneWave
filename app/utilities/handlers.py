from importlib import resources
import discord.ext.commands as commands

BLACKLIST = ["__init__.py", "base"]
BASE_PACKAGE = "app.core"

filter = lambda x: [file[:-3] for file in x if file.endswith(".py") and file not in BLACKLIST]

# This is pretty verbose, maybe doing it as a class will be better


def load_commands(client: commands.Bot):
    commands = resources.contents(f"{BASE_PACKAGE}.commands")
    commands = filter(commands)

    for command in commands:
        client.load_extension(f"{BASE_PACKAGE}.commands.{command}")


def load_events(client: commands.Bot):
    events = resources.contents(f"{BASE_PACKAGE}.events")
    events = filter(events)

    for event in events:
        client.load_extension(f"{BASE_PACKAGE}.events.{event}")


def load_modules(client: commands.Bot):
    modules = resources.contents(f"{BASE_PACKAGE}.modules")
    modules = filter(modules)

    for module in modules:
        client.load_extension(f"{BASE_PACKAGE}.modules.{module}")
