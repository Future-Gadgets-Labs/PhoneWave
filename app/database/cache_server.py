"""Used to Cache things to redis"""

from typing import Any
from redis import Redis as CacheServer

from app.config import config
from structlog import get_logger


logger = get_logger(group="cache")


class RedisCache:
    """Handle the cache managment"""

    _cache: CacheServer = None
    namespace = None
    expiry = None

    # Default expire time is 24hours
    def __init__(self, namespace: str = None, expiry: int = 24 * 60 * 60) -> None:
        self.namespace = namespace
        self.expiry = expiry

    def init(self):
        RedisCache._cache = CacheServer(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True,
        )

        logger.info("Attempting to connect to Redis...")

        try:
            RedisCache._cache.ping()
            logger.info("Redis connected successfully.")
        except Exception as e:
            logger.critical(e)
            logger.critical("Redis is not running. Please start it.")
            exit(1)

    def namespaced_key(self, key: str) -> str:
        """If a namespace is set, prefix the key with it"""

        if self.namespace is not None:
            key = key + self.namespace

        return key

    def get(self, key: str, default_value: Any = None) -> Any:
        """Get a value from the cache"""

        key = self.namespaced_key(key)
        value = self._cache.get(key)

        if value is None and default_value is not None:
            value = default_value

        return value

    def set(self, key: str, value: Any, **kwargs) -> None:
        """Set a value in the cache"""
        expiry = kwargs.pop("ex", self.expiry)

        key = self.namespaced_key(key)
        self._cache.set(key, value, ex=expiry)
