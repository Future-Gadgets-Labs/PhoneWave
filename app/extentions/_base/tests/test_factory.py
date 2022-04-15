import pytest
import discord.ext.test as testcord

from app.types.discord import Command
from ..utilities import factory


# Factory / Commands


async def test_can_register_command(client):
    """Checks if the decorators registers the command"""

    @factory.register_command()
    async def test_command(ctx):
        ctx.send("test")

    assert isinstance(test_command, Command)
    assert test_command.name == "test_command"

    await testcord.message("p!test_command")


def test_can_register_command_with_name():
    """Checks if the decorators registers the command with a name"""

    @factory.register_command(name="rand_name")
    async def test_command(ctx):
        pass

    assert isinstance(test_command, Command)
    assert test_command.name == "rand_name"


# Factory / Events
def test_can_register_event(client):
    """Checks if the decorators registers the event"""

    @factory.register_event(name="on_message")
    async def on_message(ctx):
        pass

    assert on_message.name == "test_event"
