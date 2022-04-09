class Config:
    # Bot settings
    BOT_ENV = "development"  # development, production, testing
    BOT_TOKEN = None
    BOT_PREFIX = "p!"
    BOT_DEVS_ID = None

    # MongoDB stuff
    MONGO_URI = None

    @staticmethod
    def overwrite(**kwargs):
        for key, value in kwargs.items():
            setattr(Config, key, value)


config = Config()
