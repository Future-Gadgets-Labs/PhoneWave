import mongoengine

from app.exceptions import BadConfig
from app.utilities import logger
from app.config import config


def init():
    if not config.MONGO_URI:
        raise BadConfig("MONGO_URI is not set.")

    try:
        mongoengine.connect("phonewave", host=config.MONGO_URI)
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.critical(e)
        exit(1)
