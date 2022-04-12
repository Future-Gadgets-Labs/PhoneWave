import os

from dotenv import dotenv_values
from .cli import cli_runner
from .utilities import emoji


class Config:
    # Bot settings
    BOT_ENV = "development"  # development, production, testing
    BOT_TOKEN = None
    BOT_PREFIX = "p!"
    BOT_DEVS_ID = "100173058764976128|179480292413800448"

    # Rank system
    RANK_XP_TIMEOUT = 5 # Time in seconds
    RANK_XP_REWARD = 15 # XP reward
    
    # Announcement
    ANNOUNCEMENT_WELCOME = f"Everyone, welcome lab member #{{number}}, {{name}}! {emoji.smug_okabe_emoji}"
    ANNOUNCEMENT_FAREWELL = f"It is with great sorrow that I say farewell to lab member #{{number}}, {{name}}. {emoji.dark_okabe_emoji}"

    # MongoDB
    MONGO_URI = None
    MONGO_DB = "phonewave"

    # Redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0

    def __init__(self, *args, **kwargs):
        # Overwrite the config with the environment file [.env]
        # Overwrite the config with the sys' environment variables
        # Overwrite the config with the CLI arguments
        self.set_list(**dotenv_values())  # load .env file
        self.set_list(**os.environ)       # load environment variables
        cli_runner(self)                  # load CLI arguments

    def set(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def set_list(self, **kwargs):
        for key, value in kwargs.items():
            self.set(key, value)


config = Config()
