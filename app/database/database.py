import mongoengine

from app.exceptions import BadConfig
from app.utilities import logger
from app.config import config


def init():
    if not config.MONGO_DB:
        raise BadConfig("MONGO_DB is not set.")
    if not config.MONGO_URI:
        raise BadConfig("MONGO_URI is not set.")

    try:
        mongoengine.connect(db=config.MONGO_DB, host=config.MONGO_URI, uuidRepresentation="standard")
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.critical(e)
        exit(1)
