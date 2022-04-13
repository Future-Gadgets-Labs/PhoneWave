import logging
import typing

import discord
from discord import Member as DiscordMember
from discord import User as DiscordUser
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext

from app import client
from app.database.models import Member
from app.utilities.cogs import defer


class Profile(commands.Cog):
    def __init__(self, bot: client.PhoneWave):
        self.bot = bot

    async def force_sync(self, guild_id=None):
        # TODO
        # logger.info(f"[user] Synced {len(self.roles)} members")
        pass

    @bridge.bridge_command()
    @discord.option(name="user", description="The user. If none selected, defaults to the caller")
    @discord.option(name="lab_member_number", description="The lab member number")
    async def profile(
        self,
        ctx: BridgeContext,
        user: typing.Union[DiscordMember, DiscordUser] = None,
        lab_member_number: int = None
    ):
        """See user profile."""
        await defer(ctx)

        # Default to the caller if no `user` or `number` was provided
        if not user and not lab_member_number:
            user = ctx.author

        db_member = None
        if user is not None:
            db_member = Member.get_member(ctx.guild.id, user.id, create=False)
        elif lab_member_number is not None:
            db_member = Member.get_member_by_labmem_number(ctx.guild.id, lab_member_number)

        if not db_member:
            await ctx.respond(f"No information found for {user.name}.")
            return

        embed = discord.Embed()
        embed.add_field(name="Lab Member", value=f"#{db_member.lab_member_number:03d}", inline=False)
        embed.add_field(name="Joined", value=db_member.joined_at, inline=False)
        embed.add_field(name="Is Active?", value=db_member.is_active, inline=False)
        embed.add_field(name="Is Veteran?", value=db_member.is_veteran, inline=False)

        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="user_list")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def list(self, ctx: BridgeContext):
        """Lists all users in this server."""
        await defer(ctx)
        await ctx.respond(f"USER LIST.")  # TODO

    @bridge.bridge_command(name="user_sync")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: BridgeContext):
        """Forces a resync on all users in this server."""
        await defer(ctx)
        await self.force_sync(ctx.guild.id)
        await ctx.respond("All users on this server have been sync'd!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.force_sync()

    # TODO: listen for nick changes


def setup(bot: client.PhoneWave):
    bot.add_cog(Profile(bot))
