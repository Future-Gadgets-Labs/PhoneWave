import os

from dotenv import dotenv_values
from .cli import cli_runner


class Config:
    # Bot settings
    BOT_ENV = "development"  # development, production, testing
    BOT_TOKEN = None
    BOT_PREFIX = "p!"
    BOT_DEVS_ID = "100173058764976128|179480292413800448"

    # MongoDB stuff
    MONGO_URI = None
    MONGO_DB = "phonewave"

    @staticmethod
    def overwrite(**kwargs):
        for key, value in kwargs.items():
            if not key.startswith("BOT_") and not key.startswith("MONGO_"):
                continue  # ignore non-app configs
            setattr(Config, key, value)


config = Config()
config.overwrite(**dotenv_values())  # load .env file
config.overwrite(**os.environ)       # load environment variables
cli_runner(config)
