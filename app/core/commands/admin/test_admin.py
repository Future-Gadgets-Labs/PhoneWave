import pytest
from unittest import mock
from unittest.mock import MagicMock
from discord.ext import commands

from .admin import BotCommand


@pytest.mark.asyncio
async def test_testing(monkeypatch):
    assert False
