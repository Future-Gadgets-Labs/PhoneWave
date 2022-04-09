from app import PhoneWave, config, cli


cli.cli_runner(config)


# from app.utilities import logger
# from app.exceptions import BadConfig

print(config.BOT_TOKEN)

# if __name__ == "__main__":
#     logger.info("Starting up...")

#     try:
#         PhoneWave().run()
#     except BadConfig as e:
#         logger.critical(e)
#     except Exception as e:
#         logger.exception(e)
