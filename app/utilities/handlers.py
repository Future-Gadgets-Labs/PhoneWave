from pathlib import Path

import discord.ext.commands as commands

from .logger import logger
from .bannana_catcher import bannana_catcher

BLACKLIST = ["__pycache__", "__init__"]
ROOT_PATH = Path(__file__).parent.parent

filter = lambda files: [file for file in files if file not in BLACKLIST]


@bannana_catcher
def load_modules(client: commands.Bot):
    packages = ROOT_PATH / "modules"
    modules = filter([folder.name for folder in packages.iterdir() if folder.is_dir()])

    loaded = []

    for module in modules:
        package = packages / module
        extensions = filter([file.stem for file in package.iterdir() if file.is_file()])
        failed = []

        for extension in extensions:
            try:
                client.load_extension(f"app.modules.{module}.{extension}")
                loaded.append({"module": module, "extension": extension})
            except Exception as e:
                failed.append({"module": module, "extension": extension, "error": e})

        if failed:
            logger.error(f"Failed to load {len(failed)} extensions from [{module}]:")
            logger.error("-----")

            for extension in failed:
                logger.error(f"Failed to load {extension['module']}.{extension['extension']}")
                logger.error(f"{extension['error']}")
                logger.error(" ")

    logger.info(f"Loaded {len(loaded)} extensions.")
