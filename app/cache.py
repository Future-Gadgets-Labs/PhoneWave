import redis
from discord import Guild as DiscordGuild
from discord import Member as DiscordMember

from app.utilities import logger
from .config import config

cache = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)


def check():
    try:
        cache.ping()
        logger.info("Redis connected successfully.")
    except Exception as e:
        logger.critical(e)
        logger.critical("Redis is not running. Please start it.")
        exit(1)

def format_key(key, guild:DiscordGuild=None, member:DiscordMember=None):
    if guild != None:
        key += ":g!" + str(guild.id)

    if member != None:
        key += ":u!" + str(member.id)

    return key

def cache_get(key, default_value, guild:DiscordGuild=None, member:DiscordMember=None, should_add_value_if_missing:bool=True):
    formatted_key = format_key(key, guild, member)
    value = cache.get(formatted_key)

    if not value:
        value = default_value

        if should_add_value_if_missing:
            cache.set(formatted_key, value)

    return value

def cache_set(key, value, guild:DiscordGuild=None, member:DiscordMember=None):
    formatted_key = format_key(key, guild, member)
    cache.set(formatted_key, value)