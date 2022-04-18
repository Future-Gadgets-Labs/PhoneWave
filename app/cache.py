import logging
from typing import Union

from redis import Redis as CacheServer
from discord import Guild as DiscordGuild, Member as DiscordMember, User as DiscordUser

from .config import config
from .utilities.logger import LEVEL_TRACE
from app.utilities import logger

cache = None

REDIS_PORT = config.REDIS_PORT
REDIS_HOST = config.REDIS_HOST
REDIS_DB = config.REDIS_DB

def init(is_testing: bool):
    global cache
    if is_testing:
        from vendor.mockredis import MockServer as MockCache  # In here since we won't be in testing in public
        cache = MockCache(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)
    else:
        cache = CacheServer(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)

    try:
        cache.ping()
        logger.info("Redis connected successfully.")
    except Exception as e:
        logger.critical(e)
        logger.critical("Redis is not running. Please start it.")
        exit(1)

def format_key(key: str, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None) -> str:
    if guild is not None:
        key += ":g!" + str(guild.id)

    if user is not None:
        key += ":u!" + str(user.id)

    return key


def cache_get(
    key: str,
    default_value=None,
    guild: DiscordGuild = None,
    user: Union[DiscordMember, DiscordUser] = None,
    should_add_value_if_missing: bool = True,
) -> str | None:
    formatted_key = format_key(key, guild, user)
    value = cache.get(formatted_key)

    if not value and default_value is not None:
        value = default_value

        if should_add_value_if_missing:
            cache.set(formatted_key, value)

    return value


def cache_set(key: str, value, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
    formatted_key = format_key(key, guild, user)
    logging.log(LEVEL_TRACE, f"[cache] SET {formatted_key} = {value}")

    if value is not None:
        cache.set(formatted_key, value)


def cache_delete(key: str, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
    formatted_key = format_key(key, guild, user)
    logging.log(LEVEL_TRACE, f"[cache] DELETE {formatted_key}")
    cache.delete(formatted_key)


def cache_get_dict(
    key: str, default_value=None, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None
) -> dict | None:
    formatted_key = format_key(key, guild, user)
    value = cache.hgetall(formatted_key)
    return value or default_value or {}


def cache_set_dict(key: str, value: dict, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
    formatted_key = format_key(key, guild, user)
    logging.log(LEVEL_TRACE, f"[cache] SET DICT {formatted_key} = {value}")
    for k, v in value.items():
        if v is not None:
            cache.hset(formatted_key, k, v)
