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

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")


def setup(bot):
    bot.add_cog(ClientEvents(bot))
