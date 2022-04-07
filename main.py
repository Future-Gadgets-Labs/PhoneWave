import asyncio
import os

from dotenv import load_dotenv

from app import PhoneWave
from app.utilities import logger


load_dotenv(".env")
load_dotenv(".env.development")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = PhoneWave(loop=loop, command_prefix=os.getenv("PREFIX"))

    try:
        loop.run_until_complete(client.run(os.getenv("TOKEN")))
    except RuntimeError:
        exit(0)
