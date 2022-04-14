import glob

import pytest
import discord.ext.test as testcord

from app import PhoneWave
from app.config import config

@pytest.fixture
def mock_phonewave(event_loop):
    config.MONGO_URI = "mongomock://localhost/"
    mock_phonewave = PhoneWave(loop=event_loop)
    testcord.configure(mock_phonewave)
    return mock_phonewave


def pytest_sessionfinish():
    files = glob.glob('./testcord_*.dat')
    for path in files:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error while deleting file {path}: {e}")