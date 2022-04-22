import discord
from discord.ext import commands
from discord.ext.commands import Context

from app.utilities import logger
import app.utilities.drawing.master as drawing


ContextType = commands.Context


def profileCardFromMember(member):

    # getting user's server specific nickname (if it's not set, then just getting his general discord name)
    nickname = member.nick
    if not nickname:
        nickname = member.name

    return discord.File(
        drawing.drawProfileCard(
            member.avatar.url,
            nickname,
            member.discriminator
        ), filename="profile_card.png" )

class Hiddenprofilecard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    #async def hiddenprofilecard(self, ctx: Context):
    async def hpc(self, ctx: Context, member: discord.Member = None):
        logger.info("Received 'Hiddenprofilecard' command...")

        # checking if any mentions were sent
        if ctx.message.mentions:
            for mention in ctx.message.mentions:
                await ctx.send(file = profileCardFromMember(mention))
        else:
            await ctx.send(file = profileCardFromMember(ctx.message.author))
        return True


def setup(bot):
    bot.add_cog(Hiddenprofilecard(bot))
