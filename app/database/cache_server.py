"""Used to Cache things to redis"""

from typing import Any
from redis import Redis as CacheServer

from app.types.discord import DiscordMember, DiscordGuild, DiscordUser
from app.config import config
from app.utilities.logger import LEVEL_TRACE
from app.utilities import logger


_cache: CacheServer = None


class RedisCache:
    """Handle the cache managment"""

    namespace = None
    expiry = None

    # Default expire time is 24hours
    def __init__(self, namespace: str = None, expiry: int = 24 * 60 * 60) -> None:
        self.namespace = namespace
        self.expiry = expiry

    def init(self):
        _cache = CacheServer(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True,
        )

        logger.info("Attempting to connect to Redis...", group="cache")

        try:
            _cache.ping()
            logger.info("Redis connected successfully.", group="cache")
        except Exception as e:
            logger.critical(e, group="cache")
            logger.critical("Redis is not running. Please start it.", group="cache")
            exit(1)

    def namespaced_key(self, key: str) -> str:
        """If a namespace is set, prefix the key with it"""

        if self.namespace is not None:
            key = self.namespace + key

        return key

    @classmethod
    def get(cls, key: str, default_value: Any = None) -> Any:
        """Get a value from the cache"""

        key = cls.namespaced_key(key)
        value = _cache.get(key)

        if value is None and default_value is not None:
            value = default_value

        return value

    @classmethod
    def set(cls, key: str, value: Any, *, **kwargs) -> None:
        """Set a value in the cache"""
        expiry = kwargs.pop("ex", cls.expiry)
        
        key = cls.namespaced_key(key)
        _cache.set(key, value, ex=expiry)


_cache.set

server_cache = RedisCache(":g:")
user_cache = RedisCache(":u:")
cache = RedisCache
