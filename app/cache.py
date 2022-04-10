import redis

from app.utilities import logger
from .config import config

prefix_db = None


def init():
    global prefix_db
    prefix_db = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_PREFIX_DB, decode_responses=True)
    check()


def check():
    try:
        prefix_db.ping()
        logger.info("Redis connected successfully.")
    except Exception as e:
        logger.critical(e)
        logger.critical("Redis is not running. Please start it.")
        exit(1)
