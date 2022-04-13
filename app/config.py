from dotenv import dotenv_values
from app.utilities import SingletonMeta

temp = dotenv_values()


class Config(metaclass=SingletonMeta):
    # Bot settings
    BOT_ENV = "development"  # development, production, staging, testing
    BOT_TOKEN = temp.get("BOT_TOKEN", None)
    BOT_PREFIX = "p!"
    BOT_DEVS_ID = "100173058764976128|179480292413800448"

    # Rank system
    RANK_XP_TIMEOUT = 5  # Time in seconds
    RANK_XP_REWARD = 15  # XP reward

    # MongoDB
    MONGO_URI = None
    MONGO_DB = "phonewave"

    # Redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
