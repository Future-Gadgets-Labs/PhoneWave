import redis as cache_server

from .config import config
from app.utilities import logger

# no clue how to call it for now,

redis = cache_server.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)


def check_redis():
    try:
        redis.ping()
        logger.info("Redis connected successfully.")
    except Exception as e:
        logger.critical(e)
        logger.critical("Redis is not running. Please start it.")
        exit(1)
