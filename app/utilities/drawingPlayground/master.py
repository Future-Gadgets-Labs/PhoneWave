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
    alpha_bg = PIL.Image.new(mode="RGBA", size=blurred_img.size, color=(18, 17, 21, 127))
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

    for i in range(0,7):
        additional_x_offset = i * 10 + i * constants.badge_size[0]
        badge_offset = (constants.first_badge_offset[0] + additional_x_offset, constants.first_badge_offset[1])
        background = drawBadgeBackgroundOnBackground(badge_offset, background)

    # creating pfp circle https://stackoverflow.com/a/22336005/11273040 and pasting it on background
    bigsize = (pfp_original.size[0] * 2, pfp_original.size[1] * 2)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)

    mask = mask.resize(constants.pfp_circle_size, Image.Resampling.LANCZOS)
    pfp_circle = ImageOps.fit(pfp_original, mask.size, centering=(0.5, 0.5))
    pfp_circle.putalpha(mask)

    alpha_bg = PIL.Image.new(mode="RGBA", size=background.size, color=(0, 0, 0, 0))
    alpha_bg.paste(pfp_circle, constants.pfp_circle_offset)
    background = Image.alpha_composite(background, alpha_bg)

    # progress bar
    progress_bar_xp = createProgressBar(87, constants.xp_bar_size, background.size, constants.xp_bar_offset)
    background = Image.alpha_composite(background, progress_bar_xp)


    # drawing texts
    draw = ImageDraw.Draw(background)

    # checking if nickname provided is longer than 9, if so then it needs to be cut and 3 dots need to be added
    if len(nickname) > 12:
        nickname = nickname[0:12] + "..."

    drawText(nickname, 32, (24, 56), 'ExtraBold', draw)
    drawText(str(discriminator)+"  |  "+str(labmem_number), 20, (24, 96), 'Regular', draw)

    drawText("LEVEL", 16, (40, 198), 'Regular', draw)
    drawText(str(level), 20, (50, 222), 'ExtraBold', draw)
    drawText("XP", 12, (100, 176), 'Regular', draw)
    drawText("Level", 12, (100, 217), 'Regular', draw)
    drawText("Rank", 12, (100, 236), 'Regular', draw)
    drawText("Messages Sent", 12, (100, 255), 'Regular', draw)
    drawText("Badges Acquired", 12, (36, 304), 'Regular', draw)


    # progress bar values (I don't use drawText, because it's simpler to handle anhors and aligns just this way)
    font = ImageFont.truetype(constants.default_font, 12)
    font.set_variation_by_name('ExtraBold')
    draw.text((380, 178),"54.2K / 60K",font=font, align="right", anchor="rt")
    draw.text((380, 219),"89",font=font, align="right", anchor="rt")
    draw.text((380, 238),"#2",font=font, align="right", anchor="rt")
    draw.text((380, 257),"235K",font=font, align="right", anchor="rt")
    draw.text((380, 306),"5/7",font=font, align="right", anchor="rt")


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
