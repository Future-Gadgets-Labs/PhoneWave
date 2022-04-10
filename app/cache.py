import redis as cache_server
from .config import config

# no clue how to call it for now,

redis = cache_server.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)
