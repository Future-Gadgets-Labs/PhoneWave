import discord
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeContext

from app import client
from app.database.models import Guild, Role as RoleDB
from app.utilities import logger
from app.utilities.cogs import defer


class Role(commands.Cog):
    def __init__(self, bot: client.PhoneWave):
        self.bot = bot
        self.roles = {}

    async def load(self):
        for db_guild in Guild.objects:
            guild = self.bot.get_guild(db_guild.guild_id)

            for db_role in db_guild.roles:
                role = discord.utils.get(guild.roles, id=db_role.role_id)

                key = (db_guild.guild_id, db_role.channel_id, db_role.message_id, db_role.emoji_id)
                self.roles[key] = role

                logger.debug(f"[role] Loaded role '{role}'")

        logger.info(f"[role] Loaded {len(self.roles)} roles")

    async def force_resync(self, resync_guild_id=None):
        for key, role in list(self.roles.items()):
            users_with_role = set(role.members)
            users_with_reaction = set()

            guild_id = key[0]
            channel_id = key[1]
            message_id = key[2]
            emoji_id = key[3]

            if resync_guild_id and resync_guild_id != guild_id:
                continue

            # Fetch all users that requested to have this role
            guild = self.bot.get_guild(guild_id)
            channel = guild.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            for reaction in message.reactions:
                if reaction.emoji.id != emoji_id:
                    continue

                async for user in reaction.users():
                    users_with_reaction.add(user)

            # Add missing roles
            for user in users_with_reaction:
                if user.bot:
                    continue
                has_role = next((True for u in users_with_role if u.id == user.id), False)
                if not has_role:
                    await user.add_roles(role)
                    logger.debug(f"[role] Adding role '{role}' to user '{user}'")

            # Remove outdated roles
            for user in users_with_role:
                should_have_role = next((True for u in users_with_reaction if u.id == user.id), False)
                if not should_have_role:
                    await user.remove_roles(role)
                    logger.debug(f"[role] Removing role '{role}' to user '{user}'")

            logger.debug(f"[role] Resynced role '{role}'")

        logger.info(f"[role] Resynced {len(self.roles)} roles")

    async def assign_role(
        self,
        guild: discord.Guild,
        role: discord.Role,
        emoji: discord.Emoji,
        message: discord.Message,
    ):
        # Add role to database
        db_role = RoleDB(role_id=role.id, channel_id=message.channel.id, message_id=message.id, emoji_id=emoji.id)

        db_guild = Guild.objects(guild_id=guild.id).first()
        if not db_guild:
            db_guild = Guild(guild_id=guild.id, prefix=None, roles=[])

        db_guild.roles.append(db_role)
        db_guild.save()

        # Add role to internal dict
        key = (db_guild.id, message.channel.id, message.id, emoji.id)
        self.roles[key] = role

        # Add reaction to message
        await message.add_reaction(emoji)

        logger.info(f"[role] Role '{role}' assigned to emoji '{emoji}' on message {message.id} on guild {db_guild.id}")

    async def unassign_role(
        self,
        guild: discord.Guild,
        role: discord.Role,
    ):
        # Remove role from database
        db_guild = Guild.objects(guild_id=guild.id).first()
        if db_guild:
            deleted_role = False
            for db_role in list(db_guild.roles):
                if db_role.role_id == role.id:
                    db_guild.roles.remove(db_role)
                    deleted_role = True

            if deleted_role:
                db_guild.save()

        # Remove role from internal dict
        for k, r in list(self.roles.items()):
            if r.id == role.id:
                del self.roles[k]

        logger.info(f"[role] Role '{role}' unassigned on guild {guild.id}")

    def get_assigned_role(self, guild_id, channel_id, message_id, emoji_id):
        key = (guild_id, channel_id, message_id, emoji_id)
        return self.roles.get(key)

    @bridge.bridge_command(name="role_assign")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @discord.option(name="role", description="The self-service role")
    @discord.option(name="emoji", description="The emoji used to add the role")
    @discord.option(name="message", description="The message to listen for the emoji")
    async def assign(
        self,
        ctx: BridgeContext,
        role: discord.Role,
        emoji: discord.Emoji,
        message: discord.Message
    ):
        """Create a new self-service role."""
        await defer(ctx)

        if message is None and ctx.message.reference is not None:
            message = ctx.message.reference.resolved

        if role is None:
            await ctx.reply(f"You're missing a role.")
            return
        if emoji is None:
            await ctx.reply(f"You're missing an emoji.")
            return
        if message is None:
            await ctx.reply(f"You're missing a message. Reply to the message or paste a link to it.")
            return

        if not role.is_assignable():
            await ctx.reply(f"This role cannot be assigned by the bot.")
            return

        await self.assign_role(ctx.guild, role, emoji, message)

        await ctx.respond(f"Assigning {role.mention} to all users that react with {emoji}.")
        await message.reply(f"Self-service role {role} with emoji {emoji} to this message is now ready.", delete_after=30)

    @bridge.bridge_command(name="role_unassign")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @discord.option(name="role", description="The self-service role")
    async def unassign(self, ctx: BridgeContext, role: discord.Role):
        """Remove self-service role."""
        await defer(ctx)

        if role is None:
            await ctx.reply(f"You're missing a role.")
            return

        # Remove bot reaction from message
        for key, r in list(self.roles.items()):
            guild_id = key[0]
            channel_id = key[1]
            message_id = key[2]
            emoji_id = key[3]

            if guild_id != ctx.guild.id or r.id != role.id:
                continue

            channel = ctx.guild.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            emoji = ctx.bot.get_emoji(emoji_id)
            await message.remove_reaction(emoji, self.bot.user)

        # Remove role assignment from database
        await self.unassign_role(ctx.guild, role)

        await ctx.respond(f"All mentions to the self-service role {role.mention} have been removed.")

    @bridge.bridge_command(name="role_list")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def list(self, ctx: BridgeContext):
        """List of all the self-service roles configured on this server."""
        await defer(ctx)

        embed = discord.Embed()

        is_first = True
        for key, role in self.roles.items():
            guild_id = key[0]
            emoji_id = key[3]

            if guild_id != ctx.guild.id:
                continue

            emoji = ctx.bot.get_emoji(emoji_id)

            embed.add_field(name="Role" if is_first else "\u200b", value=role.mention, inline=True)
            embed.add_field(name="Emoji" if is_first else "\u200b",
                            value=f"<:{emoji.name}:{emoji.id}> `:{emoji.name}:`", inline=True)
            embed.add_field(name="\u200b", value=f"\u200b")  # spacer

            is_first = False

        if len(self.roles) < 1:
            embed.add_field(name="Role", value="There are no self-service roles configured.")

        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="role_resync")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)  
    async def resync(self, ctx: BridgeContext):
        """Resync all self-service roles in this server"""
        await defer(ctx)

        await self.force_resync(resync_guild_id=ctx.guild.id)

        await ctx.respond("All roles managed on this guild have been resync'd!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load()
        await self.force_resync()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        role = self.get_assigned_role(payload.guild_id, payload.channel_id, payload.message_id, payload.emoji.id)
        if role is not None:
            await payload.member.add_roles(role)
            logger.info(f"[role] Added role '{role}' to '{payload.member}' on guild {payload.guild_id}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        role = self.get_assigned_role(payload.guild_id, payload.channel_id, payload.message_id, payload.emoji.id)
        if role is not None:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            logger.info(f"[role] Removed role '{role}' from '{member}' on guild '{guild}'")


def setup(bot: client.PhoneWave):
    bot.add_cog(Role(bot))
