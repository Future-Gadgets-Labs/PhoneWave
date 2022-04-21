import discord
from discord.ext import commands
from discord.ext.commands import Context

from app.utilities import logger
import app.utilities.drawing.master as drawing


ContextType = commands.Context


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
                profile_card = discord.File( drawing.drawProfileCard(mention.avatar.url), filename="profile_card.png" )
                await ctx.send("SEX", file=profile_card)
            return True
        else:
            return await ctx.send(ctx.message.author.avatar.url)


def setup(bot):
    bot.add_cog(Hiddenprofilecard(bot))
