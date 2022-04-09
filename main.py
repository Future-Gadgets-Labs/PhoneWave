from dotenv import dotenv_values

from app import cli, PhoneWave, config
from app.utilities import logger
from app.exceptions import BadConfig

config.overwrite(**dotenv_values())
cli.cli_runner(config)

print(config.BOT_TOKEN)

# if __name__ == "__main__":
#     logger.info("Starting up...")

#     try:
#         PhoneWave().run()
#     except BadConfig as e:
#         logger.critical(e)
#     except Exception as e:
#         logger.exception(e)
