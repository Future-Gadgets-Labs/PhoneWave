import discord
from discord.ext import commands
from discord.ext.commands import Context

from app.types.discord import DiscordMember
from app.utilities import logger
from app.drawing.profilecard.master import draw_profile_card


def profileCardFromMember(member):

    #######################################################
    #  TODO!!! REPLACE PLACEHOLDER VALUES WITH REAL ONES  #
    #######################################################
    print(member)
    return discord.File(
        draw_profile_card(
            member.avatar.url,  # avatar
            member.display_name,  # nickname
            member.discriminator,  # discriminator
            222,  # lab mem
            21,  # level
            1,  # rank
            235621,  # messages sent
            54200,  # xp current
            60000,  # next level xp
            [
                "operation_elysian_veteran",
                "daru69",
            ],  # Acquired badges names, they represent file as shown in constants.badges_map
        ),
        filename="profile_card.png",
    )


class Profilecard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profilecard(self, ctx: Context, member: DiscordMember = None):
        logger.info("Received 'profilecard' command...")

        if ctx.message.mentions:
            for mention in ctx.message.mentions:
                await ctx.send(file=profileCardFromMember(mention))
        else:
            await ctx.send(file=profileCardFromMember(ctx.message.author))
        return True


def setup(bot):
    bot.add_cog(Profilecard(bot))
