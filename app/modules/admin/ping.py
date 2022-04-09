import discord
from discord.ext import commands

from app.utilities import logger

ContextType = commands.Context


class BotCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: ContextType):
        logger.info("Received 'testing' command...")
        return await ctx.send("Hello World 🥼")

    @commands.command()
    async def user(self, ctx: ContextType, action=None, user: discord.Member = None):
        logger.info(f"User command with action '{action}' and user '{user}'")

        if user is None:
            user = ctx.author

        if action == "info":
            msg = f"{user} joined on {user.joined_at} and has {len(user.roles)} roles."
            return await ctx.send(msg)
        elif action == "add":
            db_user = {
                "id": user.id,
                "display_name": user.display_name,
                "name": user.name,
                "discriminator": user.discriminator,
                "joined_at": user.joined_at,
                "labmem_number": -1,
                "is_veteran": False,
            }

            if self.bot.db.users.find({"id": user.id}):
                self.bot.db.users.delete_one({"id": user.id})

            self.bot.db.users.insert_one(db_user)
            return await ctx.send(f"{user} added:\n```json\n{db_user}```")
        elif action == "remove":
            self.bot.db.users.delete_one({"id": user.id})
            return await ctx.send(f"{user} removed")
        else:
            msg = f"Usage:\n- info [user]\n- add [user]\n- remove [user]"
            return await ctx.send(msg)


def setup(bot):
    bot.add_cog(BotCommand(bot))
