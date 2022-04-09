import mongoengine

from app.exceptions import BadConfig
from app.utilities import logger
from app.config import config


if not config.MONGO_URI:
    raise BadConfig("MONGO_URI is not set.")


def init():
    try:
        mongoengine.connect("phonewave", host=config.MONGO_URI)
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.critical(e)
        exit(1)


# def get_client(config):
#     logger.info("Connecting to database '{}' with username '{}'".format(config.get("mongo_uri"), config.get("mongo_username")))

#     client = MongoClient(
#         host=config.get("mongo_uri"), username=config.get("mongo_username"), password=config.get("mongo_password")
#     )

#     return client


# def run_migrations(config):
#     logger.info(f"Running database migrations...")
#     manager = MigrationManager()
#     manager.config.mongo_url = config.get("mongo_uri")
#     manager.config.mongo_database = config.get("mongo_database")
#     manager.config.mongo_username = config.get("mongo_username")
#     manager.config.mongo_password = config.get("mongo_password")
#     manager.run()
#     logger.info(f"Database migrations finished")
