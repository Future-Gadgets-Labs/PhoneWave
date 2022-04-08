from pathlib import Path

import discord.ext.commands as commands

from .logger import logger
from .bannana_catcher import bannana_catcher

BLACKLIST = ["__pycache__", "base"]
ROOT_PATH = Path(__file__).parent.parent

# could be improuved, but my brain is at 2% capacity


@bannana_catcher
def load_package(client: commands.Bot, name):
    packages = ROOT_PATH / "core" / name
    modules = [x.name for x in packages.iterdir() if x.is_dir() and x.name not in BLACKLIST]

    for module in modules:
        client.load_extension(f"app.core.{name}.{module}")

    logger.info(f"Loaded {len(modules)} modules from {name}")
