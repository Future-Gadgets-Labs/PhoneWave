import logging

import discord
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext

from app import client, config
from app.cache import cache_get, cache_set, cache_delete
from app.database.models import Badge, Guild, Member
from app.utilities import LabMember, defer
from app.types.discord import DiscordGuild, DiscordMember, DiscordTextChannel, DiscordUser


class Announcements(commands.Cog):
    def __init__(self, bot: client.PhoneWave):
        self.bot = bot
        self.default_message_templates = {
            "welcome": config.ANNOUNCEMENT_WELCOME,
            "farewell": config.ANNOUNCEMENT_FAREWELL,
        }

    def get_announcement_channel(self, guild: DiscordGuild) -> DiscordTextChannel | None:
        channel_id_str = self.get_announcement_data(guild, "channel_id")
        channel_id = int(channel_id_str) if channel_id_str else None

        if channel_id is not None:
            return self.bot.get_channel(channel_id)
        elif guild.system_channel:
            return guild.system_channel
        else:
            return None

    @staticmethod
    def get_announcement_data(guild: DiscordGuild, announcement_type: str, default: str = None) -> str | None:
        # Fetch from cache, if available
        data = cache_get("announcements:" + announcement_type, guild=guild)

        # Fetch from the database, if available
        if data is None:
            db_guild = Guild.get_guild(guild.id, create=False)
            if db_guild is not None:
                cache_set("announcements:channel_id", db_guild.announcements.channel_id, guild=guild)
                cache_set("announcements:welcome", db_guild.announcements.welcome, guild=guild)
                cache_set("announcements:farewell", db_guild.announcements.farewell, guild=guild)
                data = cache_get("announcements:" + announcement_type, guild=guild)

        return data or default

    def get_message_template(self, guild: DiscordGuild, announcement_type: str):
        default_template = self.default_message_templates.get(announcement_type)
        return self.get_announcement_data(guild, announcement_type, default_template)

    @staticmethod
    def prepare_message(template: str, member: DiscordMember, db_member: Member):
        return template\
            .replace("{number}", f"{db_member.lab_member_number:03d}")\
            .replace("{name}", member.mention)

    async def send_announcement(self, message: str, guild: DiscordGuild):
        channel = self.get_announcement_channel(guild)

        if not channel:
            logging.debug(f"Guild '{guild}' does not have an announcements channel defined, ignoring")
            return
        
        await channel.send(message)

    async def member_joined(self, member: DiscordMember):
        # Add member to the database
        db_member = Member.get_member(member.guild.id, member.id)
        db_member.is_active = True
        if not db_member.joined_at:
            db_member.joined_at = member.joined_at
        if not db_member.lab_member_number:
            labmem = LabMember.from_name(member.display_name)
            db_member.lab_member_number = labmem.lab_member_number or Member.get_next_available_lab_member_number()
        if db_member.is_veteran():
            db_member.badges.append(Badge(name="Operation Elysian Veteran"))
            if config.BADGE_VETERAN_ROLE_ID:
                veteran_role = discord.utils.get(member.guild.roles, id=config.BADGE_VETERAN_ROLE_ID)
                if veteran_role is not None:
                    await member.add_roles(veteran_role)
        db_member.save()

        message_template = self.get_message_template(member.guild, "welcome")
        message = self.prepare_message(message_template, member, db_member)

        await self.send_announcement(message, member.guild)

    async def member_left(self, member: DiscordMember):
        # Mark member as inactive on database
        db_member = Member.get_member(member.guild.id, member.id)
        db_member.is_active = False
        db_member.save()

        message_template = self.get_message_template(member.guild, "farewell")
        message = self.prepare_message(message_template, member, db_member)

        await self.send_announcement(message, member.guild)

    @bridge.bridge_command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def announcements(self, ctx: BridgeContext):
        """See current announcement settings."""
        await defer(ctx)

        dummy_member = Member(lab_member_number=1)

        channel = self.get_announcement_channel(ctx.guild)

        welcome_template = self.get_message_template(ctx.guild, "welcome")
        welcome_example = self.prepare_message(welcome_template, ctx.author, dummy_member)

        farewell_template = self.get_message_template(ctx.guild, "farewell")
        farewell_example = self.prepare_message(farewell_template, ctx.author, dummy_member)

        await ctx.respond(f"Announcements will go to {channel.mention}.\n\n"
                          f"**Welcome**\n> {welcome_example}\n\n"
                          f"**Farewell**\n> {farewell_example}")

    @bridge.bridge_command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="type", description="The announcement type: welcome, farewell.")
    @discord.option(name="user", description="The guinea pig. Defaults to you.")
    async def announcements_trigger(self, ctx: BridgeContext, type: str = None, user: DiscordUser = None):
        """Trigger an announcement message."""
        await defer(ctx)

        if not user:
            user = ctx.author

        # Convert DiscordUser to DiscordMember
        if isinstance(user, DiscordUser):
            user = ctx.guild.get_member(user.id)

        if type == 'welcome':
            await self.member_joined(user)
        elif type == "farewell":
            await self.member_left(user)
        else:
            await ctx.respond("Unknown type. Try: welcome, farewell")

    @bridge.bridge_command(name="announcements_channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="channel", description="The channel where to announce new members")
    async def set_channel(self, ctx: BridgeContext, channel: DiscordTextChannel = None):
        """Change announcement channel."""
        await defer(ctx)

        # Update database object
        guild = Guild.get_guild(ctx.guild.id)
        guild.announcements.channel_id = channel.id if channel else None
        guild.save()

        # Update cache
        cache_set('announcements:channel', channel.id if channel else None, guild=ctx.guild)

        if channel is not None:
            await ctx.respond(f"Future announcements will be done on {channel.mention}.")
        else:
            await ctx.respond("Announcements channel has been unset.")

    @bridge.bridge_command(name="announcements_welcome")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="message", description="The welcome message, may include the variables {number} and {name}.")
    async def set_welcome(self, ctx: BridgeContext, message: str = None):
        """Change announcement welcome message."""
        await defer(ctx)

        # Update database object
        guild = Guild.get_guild(ctx.guild.id)
        guild.announcements["welcome"] = message
        guild.save()

        # Update cache
        if message is not None:
            cache_set("announcements:welcome", message, guild=ctx.guild)
        else:
            cache_delete("announcements:welcome", guild=ctx.guild)

        dummy_member = Member(lab_member_number=1)

        message_template = self.get_message_template(ctx.guild, "welcome")
        message = self.prepare_message(message_template, ctx.author, dummy_member)

        await ctx.respond(f"Example: {message}")

    @bridge.bridge_command(name="announcements_farewell")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @discord.option(name="message", description="The farewell message, may include the variables {number} and {name}.")
    async def set_farewell(self, ctx: BridgeContext, message: str = None):
        """Change announcement farewell message."""
        await defer(ctx)

        # Update database object
        guild = Guild.get_guild(ctx.guild.id)
        guild.announcements["farewell"] = message
        guild.save()

        # Update cache
        if message is not None:
            cache_set("announcements:farewell", message, guild=ctx.guild)
        else:
            cache_delete("announcements:farewell", guild=ctx.guild)

        dummy_member = Member(lab_member_number=1)
        
        message_template = self.get_message_template(ctx.guild, "farewell")
        message = self.prepare_message(message_template, ctx.author, dummy_member)

        await ctx.respond(f"Example: {message}")

    @commands.Cog.listener()
    async def on_member_join(self, member: DiscordMember):
        logging.info(f"User '{member}' joined the guild '{member.guild}'")
        await self.member_joined(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: DiscordMember):
        logging.info(f"User '{member}' left the guild '{member.guild}'")
        await self.member_left(member)


def setup(bot: client.PhoneWave):
    bot.add_cog(Announcements(bot))
