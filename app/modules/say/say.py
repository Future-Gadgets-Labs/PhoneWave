import discord
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext, BridgeApplicationContext, BridgeExtContext

from app import client
from app.utilities import emoji


class Say(commands.Cog):
    def __init__(self, bot: client.PhoneWave):
        self.bot = bot

    # @commands.has_permissions(administrator=True)  
    @bridge.bridge_command()
    @commands.guild_only()
    @discord.option(name="message", description="The message to say in chat.")
    async def say(self, ctx: BridgeContext, *, message: str):
        """Forces the bot to say whatever you desire."""
        if isinstance(ctx, BridgeExtContext):
            await ctx.message.delete()
        elif isinstance(ctx, BridgeApplicationContext):
            await ctx.respond(f"{emoji.dark_okabe_emoji}", ephemeral=True)

        await ctx.channel.send(message)


def setup(bot: client.PhoneWave):
    bot.add_cog(Say(bot))
