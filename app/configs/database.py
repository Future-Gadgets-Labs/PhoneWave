from os import environ


MONGO_URI = environ.get("MONGO_URI", "mongodb://localhost:27017/phonewave")
