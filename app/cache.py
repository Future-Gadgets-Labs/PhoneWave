from typing import Union

from redis import Redis as CacheServer
from discord import Guild as DiscordGuild, Member as DiscordMember, User as DiscordUser

from .config import config
from app.utilities import logger

cache = CacheServer(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)

REDIS_PORT = config.REDIS_PORT
REDIS_HOST = config.REDIS_HOST
REDIS_DB = config.REDIS_DB


class CacheManager:
    cache = CacheServer(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    def __init__(self, namespace=None):
        pass

r = CacheManager()


def check():
    try:
        cache.ping()
        logger.info("Redis connected successfully.")
    except Exception as e:
        logger.critical(e)
        logger.critical("Redis is not running. Please start it.")
        exit(1)


def format_key(key: str, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
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
):
    formatted_key = format_key(key, guild, user)
    value = cache.get(formatted_key)

    if not value and default_value is not None:
        value = default_value

        if should_add_value_if_missing:
            cache.set(formatted_key, value)

    return value


def cache_set(key: str, value, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
    formatted_key = format_key(key, guild, user)
    cache.set(formatted_key, value)


def cache_get_dict(key: str, default_value=None, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
    formatted_key = format_key(key, guild, user)
    value = cache.hgetall(formatted_key)
    return value if value else default_value if default_value else {}


def cache_set_dict(key: str, value: dict, guild: DiscordGuild = None, user: Union[DiscordMember, DiscordUser] = None):
    formatted_key = format_key(key, guild, user)
    for k, v in value.items():
        if v:
            cache.hset(formatted_key, k, v)
