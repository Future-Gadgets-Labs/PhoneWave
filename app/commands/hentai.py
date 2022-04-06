from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageDraw
import discord
import aiohttp
import pathlib
import os


class Hentai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testing(self, ctx):
        radius = 25
        width, height = (350, 350)

        with BytesIO() as mem:
            image = Image.new("RGBA", size=(width, height), color=(155, 0, 0))
            corner = Image.new("RGBA", (radius, radius), (0, 0, 0, 0))
            draw = ImageDraw.Draw(corner)
            draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=(155, 0, 0))
            image.paste(corner, (0, 0))
            image.paste(corner.rotate(90), (0, height - radius))
            image.paste(corner.rotate(180), (width - radius, height - radius))
            image.paste(corner.rotate(270), (width - radius, 0))

            image.save(mem, "png")
            mem.name = "test.png"
            mem.seek(0)

            return await ctx.send("1", file=discord.File(mem, mem.name))


def setup(bot):
    bot.add_cog(Hentai(bot))
