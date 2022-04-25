import sys
import os
import PIL
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageEnhance, ImageFilter
from pathlib import Path
import requests
from io import BytesIO

from utils import *
import constants

# changing import path
abspath = os.path.abspath(__file__)
ipath = os.path.dirname(abspath)
os.chdir(ipath)


def drawProfileCard(avatar_url, nickname, discriminator, labmem_number, level, rank, messages_sent, badges_list):
    # getting base images
    pfp_original = Image.open( requests.get(avatar_url, stream=True).raw )
    background = PIL.Image.new(
        mode="RGBA",
        size=constants.background_dimensions,
        color=(0, 0, 0, 255)
    )

    # scaling pfp down to around background_dimensions-ish dimensions, without streching (with maintaing aspect ratio)
    pfp_scaled = pfp_original
    base_width = constants.background_dimensions[0]
    hpercent = (base_width/float(pfp_scaled.size[1]))
    wsize = int((float(pfp_scaled.size[0])*float(hpercent)))
    pfp_scaled = pfp_scaled.resize((base_width,wsize), Image.Resampling.LANCZOS) # after this step pfp_scaled will be 513x513 square
    # putting scaled pfp on background
    background = pfp_scaled.crop((
        0, 0,
        constants.background_dimensions[0],
        constants.background_dimensions[1]
    ))

    # making background rounded rectangle (according to masks/background.png)
    background = applyAlphaWithMask(background, 'masks/background.png')


    # merging full_background (the one with alpha around it) with background (the one with all card contents in it)
    profile_card = background
    profile_card.save("final_output.png")


drawProfileCard(
    "https://cdn.discordapp.com/avatars/487896060316876800/b603f6cce63f7c6430559ae5c3a00f4b.png?size=512",
    "FreshTeaBagsByLipton",
    2036,
    222,
    21,
    1,
    235000,
    ['operation_elysian_veteran', 'daru69']
)
