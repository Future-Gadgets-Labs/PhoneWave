from app import PhoneWave
from app.utilities import logger
from app.exceptions import BadConfig


if __name__ == "__main__":
    logger.info("Starting up...")

    try:
        PhoneWave().run()
    except BadConfig as e:
        logger.critical(e)
    except Exception as e:
        logger.exception(e)
