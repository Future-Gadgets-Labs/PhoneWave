import pytest
import discord.ext.test as testcord
from app import PhoneWave


@pytest.fixture
def client(event_loop):
    client = PhoneWave(loop=event_loop)
    testcord.configure(client)
    return client
