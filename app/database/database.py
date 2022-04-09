from mongodb_migrations.cli import MigrationManager
from pymongo import MongoClient

from app.utilities import logger


def get_client(config):
    logger.info("Connecting to database '{}' with username '{}'"
                .format(config.get("mongo_uri"), config.get("mongo_username")))

    client = MongoClient(
        host=config.get("mongo_uri"),
        username=config.get("mongo_username"),
        password=config.get("mongo_password")
    )

    return client


def run_migrations(config):
    logger.info(f"Running database migrations...")
    manager = MigrationManager()
    manager.config.mongo_url = config.get("mongo_uri")
    manager.config.mongo_database = config.get("mongo_database")
    manager.config.mongo_username = config.get("mongo_username")
    manager.config.mongo_password = config.get("mongo_password")
    manager.run()
    logger.info(f"Database migrations finished")
