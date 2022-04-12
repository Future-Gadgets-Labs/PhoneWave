# Gets the required amount of xp to level up from [level - 1] to [level], or 0 if it surpasses it
from math import ceil
from sys import path as syspath
from importlib import import_module

from os.path import basename, isfile
import time as t
import glob

from discord.ext import commands

from app import client
from app.types.discord import DiscordMember, DiscordChannelType
from app.database import get_member
from app.database.ranks.baserank import BaseRank
from app.config import config
from app.cache import cache_get, cache_set
from app.utilities import logger


def get_required_xp_for_level(level, current_xp=0):
    required_xp = ceil(1.0 * (level**2) + 4.8 * level + 596)  # 1.048596
    return (required_xp - current_xp) if (required_xp > current_xp) else 0


# Table of example values:
# Level  | XP      | Total
# 1      | 596     | 596
# 2      | 602     | 1 204
# 3      | 610     | 1 830
# 4      | 620     | 2 480
# 5      | 632     | 3 160
# 10     | 721     | 7 210
# 15     | 860     | 12 900
# 20     | 1 049   | 20 980
# 25     | 1 288   | 32 200
# 50     | 3 233   | 161 650
# 100    | 10 873  | 1 087 300


class RankSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ranks = []
        filenames = glob.glob(f"{syspath[0]}\\app\\database\\ranks\\*.py")
        modules = [
            basename(f)[:-3] for f in filenames if isfile(f) and not f.endswith("__init__.py") and not f.endswith("baserank.py")
        ]

        for module in modules:
            mod = import_module("." + module, "app.database.ranks")
            register_rank = getattr(mod, "register_rank")

            if not register_rank:
                raise ValueError

            register_rank(self)

        ranks_len = len(self.ranks)
        logger.debug(f"Loaded {ranks_len} rank{'' if ranks_len == 1 else 's'} for RankSystem.")

    def add_rank(self, rank: BaseRank) -> None:
        self.ranks.append(rank)

    async def handle_rank_up(self, member: DiscordMember, level: int):
        if member != None:
            await member.send(f"Congrats on ranking up to level {level}!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
            # Don't allow self-tracking
        if message.channel.type != DiscordChannelType.text:
            return
            # Only track in guild text channels

        print(RankSystem.ranks.__len__())

        curr_time = int(t.time())

        last_xp_timestamp = int(cache_get("ranking-timeout", 0, message.guild, message.author))

        if (curr_time - last_xp_timestamp) >= config.RANK_XP_TIMEOUT:
            cache_set("ranking-timeout", curr_time, message.guild, message.author)

            member = get_member(message.guild.id, message.author.id)

            member.xp += config.RANK_XP_REWARD

            required_xp = get_required_xp_for_level(member.level)

            if member.xp >= required_xp:
                member.xp -= required_xp
                member.level += 1
                await self.handle_rank_up(message.author, member.level)

            member.save()


def setup(bot: client.PhoneWave):
    bot.add_cog(RankSystem(bot))
