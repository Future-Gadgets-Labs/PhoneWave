from discord.ext import commands
from discord.ext.bridge import BridgeContext
from discord.ext.commands import Context, CommandError

from app.utilities import logger


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_error_message(error):
        if isinstance(error, commands.CommandNotFound):
            return None  # Return because we don't want to show an error for every command not found
        elif isinstance(error, commands.CommandOnCooldown):
            return f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            return "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.UserInputError):
            return "Something about the arguments was wrong, please check the arguments and try again!"
        else:
            return "Something went wrong. Could this be sabotage done by the Organization?!..."

    @staticmethod
    def is_unknown_error(error):
        return not isinstance(error, commands.CommandNotFound)\
               and not isinstance(error, commands.CommandOnCooldown)\
               and not isinstance(error, commands.MissingPermissions)\
               and not isinstance(error, commands.UserInputError)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        """Commands error handler."""

        if ErrorHandler.is_unknown_error(error):
            logger.error(error)

        message = ErrorHandler.get_error_message(error)
        if message:
            await ctx.send(message, delete_after=30)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: BridgeContext, error: CommandError):
        """Application commands error handler."""

        if ErrorHandler.is_unknown_error(error):
            logger.error(error)

        message = ErrorHandler.get_error_message(error)
        if message:
            await ctx.respond(message, ephemeral=True)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
