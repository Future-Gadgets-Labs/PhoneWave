import os

from dotenv import load_dotenv

from app import PhoneWave
from app.utilities import logger


load_dotenv(".env")
load_dotenv(".env.development")

if __name__ == "__main__":
    bot_prefix = os.getenv("BOT_PREFIX")
    bot_token = os.getenv("BOT_TOKEN")

    client = PhoneWave(command_prefix=bot_prefix)
    client.run(bot_token)
