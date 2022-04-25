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

    pfp_scaled = ImageOps.fit(pfp_original, constants.background_dimensions)
    # putting scaled pfp on background
    background = pfp_scaled.crop((
        0, 0,
        constants.background_dimensions[0],
        constants.background_dimensions[1]
    ))

    # making background rounded rectangle (according to masks/background.png)
    background = applyAlphaWithMask(background, 'masks/background.png')

    # adding blurry region in the middle of background
    cropped_img = background.crop((
        constants.blurry_background_offset[0],
        constants.blurry_background_offset[1],
        constants.blurry_region_size[0]+constants.blurry_background_offset[0],
        constants.blurry_region_size[1]+constants.blurry_background_offset[1]
    ))

    blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(25)).convert("RGBA")
    alpha_bg = PIL.Image.new(mode="RGBA", size=blurred_img.size, color=(18, 17, 21, 150))
    blurred_img = Image.alpha_composite(blurred_img, alpha_bg)


    background.paste(
        blurred_img,
        (constants.blurry_background_offset[0], constants.blurry_background_offset[1]),
        create_rounded_rectangle_mask(blurred_img, constants.blurry_region_radius)
    )

    # adding semi-black-transparent rounded rectangle areas on top of blurried area
    background = createSemiTransparentBlackRegionOnBackground(
        constants.black_region_1_size,
        constants.black_region_1_offset,
        background
    )
    background = createSemiTransparentBlackRegionOnBackground(
        constants.black_region_2_size,
        constants.black_region_2_offset,
        background
    )

    background = drawBadgeBackgroundOnBackground(constants.badge_size, background)

    # merging full_background (the one with alpha around it) with background (the one with all card contents in it)
    profile_card = background
    profile_card.save("final_output.png")


drawProfileCard(
    #"https://cdn.discordapp.com/avatars/487896060316876800/b603f6cce63f7c6430559ae5c3a00f4b.png?size=512",
    "https://s3-alpha-sig.figma.com/img/fe2e/e3e4/1599024272626d5b9d3e84540cc950fc?Expires=1652054400&Signature=Zy8rd2lO1m0tlGxpHJoZm8SmJOd1I09aSzzDu9MBXWUL37Pe50HGebqr~17WpNHtJlWo60vcMbRSwDCF7zRhIfF5d8Ax5bRAElanwj4guzxMe9jfvaopiF8Ad1RKTkaMQzf06VX3rvQExUENDNZvJDNcxaPzksWjnPQCiqbe14-S3oO5rtjABMI8YBhPvBuUi9auaVFISvJtC9x05skwh~kdT-uKok7LIgIVIz84ej6gzgIcUl45BdPAcAXLY2Rz03QuXld7kn-6cvARPozPS2R8WzGm0aJqfTx936QD5HT~gT4zPLkQ-pd9uNS8WDHcFq6CwbxFGbJhfgq93WBJRg__&Key-Pair-Id=APKAINTVSUGEWH5XD5UA",
    "FreshTeaBagsByLipton",
    2036,
    222,
    21,
    1,
    235000,
    ['operation_elysian_veteran', 'daru69']
)
