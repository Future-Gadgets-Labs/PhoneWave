import discord
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext

from app import client
from app.cache import cache_set
from app.database.models import Guild
from app.utilities.cogs import defer


class Prefix(commands.Cog):
    def __init__(self, bot: client.PhoneWave):
        self.bot = bot

    @bridge.bridge_command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)  
    @discord.option(name="prefix", description="The new command prefix.")
    async def prefix(self, ctx: BridgeContext, *, prefix: str):
        """Changes the command prefix."""
        await defer(ctx)

        # Update database entry
        guild = Guild.get_guild(ctx.guild.id)
        guild.prefix = prefix
        guild.save()

        # Update cache
        cache_set('prefix', prefix, guild=ctx.guild)

        await ctx.respond(f"Prefix changed to `{prefix}`!")


def setup(bot: client.PhoneWave):
    bot.add_cog(Prefix(bot))
