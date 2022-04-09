import pytest


import os

from dotenv import load_dotenv

from app import PhoneWave
from app.utilities import logger

bot_prefix = os.getenv("BOT_PREFIX")
bot_token = os.getenv("BOT_TOKEN")

load_dotenv(".env")
load_dotenv(".env.development")


@pytest.fixture
def client():

    client = PhoneWave(command_prefix=bot_prefix)
    client.run(bot_token)
    return client


@pytest.fixture
def receiver():
    pass
