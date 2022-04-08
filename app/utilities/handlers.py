from genericpath import isdir
import os

from importlib import resources
import discord.ext.commands as commands

from .logger import logger
from .bannana_catcher import bannana_catcher

BLACKLIST = ["__init__.py", "base"]
BASE_PACKAGE = "app.core"


def filter(resources, package):
    isDir = lambda x: isdir(f"{package}/{x}")
    isValidFile = lambda x: x.endswith(".py") and x not in BLACKLIST
    return [file for file in resources if isDir(file) or isValidFile(file)]


# This is pretty verbose, maybe doing it as a class will be better


@bannana_catcher
def load_commands(client: commands.Bot):
    package = BASE_PACKAGE + ".commands"
    commands = filter(resources.contents(package), package)

    for command in commands:
        client.load_extension(f"{package}.{command}")

    logger.debug(f"Loaded {len(commands)} commands")


@bannana_catcher
def load_events(client: commands.Bot):
    package = BASE_PACKAGE + ".events"
    events = filter(resources.contents(package), package)

    for event in events:
        client.load_extension(f"{package}.{event}")

    logger.debug(f"Loaded {len(events)} events")


@bannana_catcher
def load_modules(client: commands.Bot):
    package = BASE_PACKAGE + ".modules"
    modules = filter(resources.contents(package), package)

    for module in modules:
        client.load_extension(f"{package}.{module}")

    logger.debug(f"Loaded {len(modules)} modules")
