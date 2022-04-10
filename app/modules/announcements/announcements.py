import logging

import discord
from discord import Guild as DiscordGuild
from discord import Member as DiscordMember
from discord import TextChannel as DiscordTextChannel
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext

from app import client, config
from app.cache import cache_get_dict, cache_set_dict
from app.database.database import get_member, get_guild
from app.database.models import Member as DatabaseMember
from app.utilities.cogs import defer


class Announcements(commands.Cog):
    def __init__(self, bot: client.PhoneWave):
        self.bot = bot

    def get_announcement_channel(self, announcement_channel_id, guild: DiscordGuild):
        if announcement_channel_id:
            return self.bot.get_channel(announcement_channel_id)
        elif guild.system_channel:
            return guild.system_channel
        else:
            return None

    def get_announcement_data(self, guild: DiscordGuild):
        data = cache_get_dict("announcements", guild=guild)

        if not data:
            db_guild = get_guild(gid=guild.id)
            data = {
                "channel_id": db_guild.announcements.channel_id,
                "welcome": db_guild.announcements.welcome,
                "farewell": db_guild.announcements.farewell,
            }
            cache_set_dict("announcements", data, guild=guild)

        channel = self.get_announcement_channel(data.get("channel_id"), guild)

        return {
            "channel": channel,
            "welcome": data.get("welcome"),
            "farewell": data.get("farewell"),
        }
    
    def replace_message_template(self, template: str, default: str, member: DiscordMember, db_member: DatabaseMember):
        if not template:
            template = default

        message = template.replace("{number}", str(db_member.lab_member_number))  # TODO: add zero-padding, e.g. 001 
        message = message.replace("{name}", member.mention)
        return message
    
    def create_member(self, member: DiscordMember):
        db_member = get_member(gid=member.guild.id, uid=member.id)
        db_member.display_name = member.display_name  # TODO: extract nick - create helper class for this
        db_member.name = member.name
        db_member.discriminator = member.discriminator
        db_member.joined_at = member.joined_at
        db_member.lab_member_number = None  # TODO: extract from nick or fetch from db if not available
        db_member.is_active = True
        db_member.is_veteran = False  # TODO: compute based on join_date
        db_member.save()
        return db_member

    @bridge.bridge_command(name="announcements")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def announcements(self, ctx: BridgeContext):
        """See current announcement settings."""
        await defer(ctx)

        announcements = self.get_announcement_data(ctx.guild)
        channel = announcements.get("channel")

        dummy_member = DatabaseMember(lab_member_number=1)
        welcome_example = self.replace_message_template(announcements.get("welcome"), config.ANNOUNCEMENT_WELCOME, ctx.author, dummy_member)
        farewell_example = self.replace_message_template(announcements.get("farewell"), config.ANNOUNCEMENT_FAREWELL, ctx.author, dummy_member)

        await ctx.respond(f"**Announcements will go to {channel.mention}.**\n\n"
                          f"Welcome\n> {welcome_example}\n\n"
                          f"Farewell\n> {farewell_example}")

    @bridge.bridge_command(name="announcements_channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="channel", description="The channel where to announce new members")
    async def set_channel(self, ctx: BridgeContext, channel: DiscordTextChannel = None):
        """Change announcement channel."""
        await defer(ctx)

        # Update database object
        guild = get_guild(gid=ctx.guild.id)
        guild.announcements.channel_id = channel.id if channel else None
        guild.save()

        # Update cache
        cached_data = cache_get_dict('announcement', {}, guild=ctx.guild)
        cached_data["channel_id"] = channel.id if channel else None
        cache_set_dict("announcement", cached_data, guild=ctx.guild)
        
        if channel:
            await ctx.respond(f"Future announcements will be done on {channel.mention}.")
        else:
            await ctx.respond("Announcements channel has been unset.")

    @bridge.bridge_command(name="announcements_welcome")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="message", description="The welcome message, may include the variables {number} and {name}.")
    async def set_welcome(self, ctx: BridgeContext, message: str):
        """Change announcement welcome message."""
        await defer(ctx)

        # Update database object
        guild = get_guild(gid=ctx.guild.id)
        guild.announcements.welcome = message
        guild.save()

        # Update cache
        cached_data = cache_get_dict("announcement", {}, guild=ctx.guild)
        cached_data["welcome"] = message
        cache_set_dict("announcement", cached_data, guild=ctx.guild)

        example = self.replace_message_template(message, config.ANNOUNCEMENT_WELCOME, ctx.author, DatabaseMember(lab_member_number=1))
        await ctx.respond(f"Example: {example}")

    @bridge.bridge_command(name="announcements_farewell")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="message", description="The farewell message, may include the variables {number} and {name}.")
    async def set_farewell(self, ctx: BridgeContext, message: str):
        """Change announcement farewell message."""
        await defer(ctx)

        # Update database object
        guild = get_guild(gid=ctx.guild.id)
        guild.announcements.farewell = message
        guild.save()

        # Update cache
        cached_data = cache_get_dict("announcement", {}, guild=ctx.guild)
        cached_data["farewell"] = message
        cache_set_dict("announcement", cached_data, guild=ctx.guild)

        example = self.replace_message_template(message, config.ANNOUNCEMENT_FAREWELL, ctx.author, DatabaseMember(lab_member_number=1))
        await ctx.respond(f"Example: {example}")

    @commands.Cog.listener()
    async def on_member_join(self, member: DiscordMember):
        logging.info(f"User '{member}' joined the guild '{member.guild}'")

        # Add member to the database
        db_member = self.create_member(member)
        # TODO: assign veteran role if is_veteran==True?

        announcements = self.get_announcement_data(member.guild)
        channel = announcements.get("channel")

        if not channel:
            logging.debug(f"Guild '{member.guild}' does not have an announcements channel defined, ignoring")
            return

        message = self.replace_message_template(announcements.get("welcome"), config.ANNOUNCEMENT_WELCOME, member, db_member)
        await channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member: DiscordMember):
        logging.info(f"User '{member}' left the guild '{member.guild}'")

        # Mark member as inactive on database
        db_member = get_member(gid=member.guild.id, uid=member.id)
        db_member.is_active = False
        db_member.save()

        announcements = self.get_announcement_data(member.guild)
        channel = announcements.get("channel")

        if not channel:
            logging.debug(f"Guild '{member.guild}' does not have an announcements channel defined, ignoring")
            return

        message = self.replace_message_template(announcements.get("farewell"), config.ANNOUNCEMENT_FAREWELL, member, db_member)
        await channel.send(message)


def setup(bot: client.PhoneWave):
    bot.add_cog(Announcements(bot))
