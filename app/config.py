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

    @staticmethod
    def overwrite(**kwargs):
        for key, value in kwargs.items():
            setattr(Config, key, value)


config = Config()
config.overwrite(**dotenv_values())
cli_runner(config)
