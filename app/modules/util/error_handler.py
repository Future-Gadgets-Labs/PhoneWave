from discord.ext import commands
from discord.ext.commands import Context, CommandError

from app.utilities import logger


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        """Global error handler."""

        if isinstance(error, commands.CommandNotFound):
            return  # Return because we don't want to show an error for every command not found
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.UserInputError):
            message = "Something about the arguments was wrong, please check the arguments and try again!"
        else:
            message = "Oh no! Could this be sabotage done by the Organization?!..."

        logger.warning(f"Command error: {error}")

        await ctx.send(message, delete_after=30)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
