"""Used to standardize the creation of commands and events"""


from discord.ext import commands


def register_command(*args, **kwargs):
    """Register a command"""

    def decorator(func):
        return commands.command(*args, **kwargs)(func)

    return decorator


def register_event(*args, **kwargs):
    """Register an event"""

    def decorator(func):
        return commands.Cog.listener(*args, **kwargs)(func)

    return decorator
