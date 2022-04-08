import os

from dotenv import load_dotenv

from app import PhoneWave
from app.utilities import logger

logger.info("Starting up...")

load_dotenv(".env")
load_dotenv(".env.development")

if __name__ == "__main__":
    try:
        bot_prefix = os.getenv("BOT_PREFIX")
        bot_token = os.getenv("BOT_TOKEN")

        client = PhoneWave(command_prefix=bot_prefix)
        client.run(bot_token)
    except Exception as e:
        logger.exception(e)
