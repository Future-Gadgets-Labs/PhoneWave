from app.utilities.logger import logger


def bannana_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.critical(e, group="bannana_catcher")

    return wrapper
