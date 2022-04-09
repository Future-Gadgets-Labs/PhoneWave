import os

from dotenv import dotenv_values

from app import PhoneWave
from app.database import database
from app.utilities import logger


def load_config():
    """Loads sane defaults to be used by the application.
    
    Order of precedence:
     - Environment variables
     - .env.development
     - .env
    """

    env = {
        **dotenv_values(".env"),
        **dotenv_values(".env.development"),
        **os.environ,
    }

    return {
        "bot_prefix": env.get("BOT_PREFIX", "p!"),
        "bot_token": env.get("BOT_TOKEN"),

        "mongo_uri": env.get("MONGO_URI"),
        "mongo_database": env.get("MONGO_DATABASE", "phonewave"),
        "mongo_username": env.get("MONGO_USERNAME"),
        "mongo_password": env.get("MONGO_PASSWORD"),
    }


if __name__ == "__main__":
    logger.info("Starting up...")
    
    try:
        config = load_config()

        database.run_migrations(config)

        client = PhoneWave(config=config)
        client.run()
    except Exception as e:
        logger.exception(e)
