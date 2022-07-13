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

    # if user has default avatar, then his .avatar is empty
    avatar_url = ""
    if member.avatar:
        avatar_url = member.avatar.url

    return discord.File(
        draw_profile_card(
            avatar_url,
            member.display_name,
            member.discriminator,
            222,
            21,
            1,
            235621,
            54200,
            60000,
            [],
        ),
        filename="profile_card.png",
    )


class Profilecard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profilecard(self, ctx: Context, member: DiscordMember = None):
        if ctx.message.mentions:
            for mention in ctx.message.mentions:
                await ctx.send(file=profileCardFromMember(mention))
        else:
            await ctx.send(file=profileCardFromMember(ctx.message.author))
        return True


def setup(bot):
    bot.add_cog(Profilecard(bot))
