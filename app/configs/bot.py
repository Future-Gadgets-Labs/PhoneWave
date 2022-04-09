from os import environ


BOT_ENV = environ.get("BOT_ENV", "development")  # development, production, testing
BOT_TOKEN = environ.get("BOT_TOKEN", None)
BOT_PREFIX = environ.get("BOT_PREFIX", "p!")
BOT_DEVS_ID = environ.get("BOT_DEVS_ID", "179480292413800448|100173058764976128")
