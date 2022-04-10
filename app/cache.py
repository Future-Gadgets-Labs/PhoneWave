import redis
from discord import Guild as DiscordGuild
from discord import Member as DiscordMember
from discord import User as DiscordUser
from typing import Union

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

def format_key(key:str, guild:DiscordGuild=None, user:Union[DiscordMember,DiscordUser]=None):
    if guild != None:
        key += ":g!" + str(guild.id)

    if user != None:
        key += ":u!" + str(user.id)

    return key

def cache_get(key:str, default_value=None, guild:DiscordGuild=None, user:Union[DiscordMember,DiscordUser]=None, should_add_value_if_missing:bool=True):
    formatted_key = format_key(key, guild, user)
    value = cache.get(formatted_key)

    if not value and default_value != None:
        value = default_value

        if should_add_value_if_missing:
            cache.set(formatted_key, value)
            
    return value

def cache_set(key:str, value, guild:DiscordGuild=None, user:Union[DiscordMember,DiscordUser]=None):
    formatted_key = format_key(key, guild, user)
    cache.set(formatted_key, value)