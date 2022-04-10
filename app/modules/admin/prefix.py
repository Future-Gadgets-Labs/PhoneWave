import discord
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext

from app import client, cache
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
        guild = Guild.objects(guild_id=ctx.guild.id).first()
        if not guild:
            guild = Guild(guild_id=ctx.guild.id, roles=[])
        guild.prefix = prefix
        guild.save()

        # Update cache
        cache.prefix_db.set(ctx.guild.id, prefix)

        await ctx.respond(f"Prefix changed to `{prefix}`!")


def setup(bot: client.PhoneWave):
    bot.add_cog(Prefix(bot))
