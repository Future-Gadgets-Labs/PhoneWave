from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageDraw
import discord
import aiohttp
import pathlib
import os


class ClientEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(ClientEvents(bot))
