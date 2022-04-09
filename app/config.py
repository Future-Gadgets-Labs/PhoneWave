from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Bot settings
    BOT_ENV = environ.get("BOT_ENV", "development")  # development, production, testing
    BOT_TOKEN = environ.get("BOT_TOKEN", None)
    BOT_PREFIX = environ.get("BOT_PREFIX", "p!")
    BOT_DEVS_ID = environ.get("BOT_DEVS_ID", "179480292413800448|100173058764976128")

    # MongoDB stuff
    MONGO_URI = environ.get("MONGO_URI", "mongodb://phonewave:changeme@localhost:27017/?authMechanism=DEFAULT")

    @staticmethod
    def update_config(key, value):
        setattr(Config, key, value)


config = Config()
