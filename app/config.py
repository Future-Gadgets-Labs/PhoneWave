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

    # Redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0

    def overwrite(self, **kwargs):
        allowed_keys = [k for k in dir(self) if not k.startswith("_") and not callable(getattr(self, k))]

        for key, value in kwargs.items():
            if key in allowed_keys:
                setattr(Config, key, value)


# Initialize the config
# Overwrite the config with the environment file [.env]
# Overwrite the config with the sys'environment variables
# Overwrite the config with the cli arguments
config = Config()
config.overwrite(**dotenv_values())
config.overwrite(**os.environ)
cli_runner(config)
