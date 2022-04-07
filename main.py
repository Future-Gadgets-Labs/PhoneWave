import asyncio
import os
import discord

from dotenv import load_dotenv

from app import PhoneWave

load_dotenv(".env")
load_dotenv(".env.development")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = PhoneWave(loop=loop, command_prefix=os.getenv("BOT_PREFIX"))

    try:
        loop.run_until_complete(client.run(os.getenv("BOT_TOKEN")))
    except RuntimeError:
        exit(0)

client = discord.Client()
