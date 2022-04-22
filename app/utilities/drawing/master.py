import sys
import os
import PIL
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageEnhance, ImageFilter
from pathlib import Path
import requests
from io import BytesIO

from .utils import *
from . import constants

# changing import path
abspath = os.path.abspath(__file__)
ipath = os.path.dirname(abspath)
os.chdir(ipath)



def drawProfileCard(avatar_url, nickname, discriminator, labmem_number):
    #####################
    #  SETTING OFFSETS  #
    #####################
    background_offset = (28, 16)
    blurry_background_offset = (12, 13)
    background_dimensions = (381, 513) # desired dimensions of card you want to crop out from 513x513 square
    radius = 16
    pfp_circle_size = (104, 104)
    pfp_circle_offset = (28, 29)
    server_circle_size = (322, 322)
    server_circle_offset = (159, 122)
    ##########################################

    # general setup of images
    font = ImageFont.truetype("fonts/Nunito-VariableFont_wght.ttf", 16)
    pfp_original = Image.open( requests.get(avatar_url, stream=True).raw )
    server_original = Image.open('server_icon.png')
    full_background = PIL.Image.new(mode="RGBA", size=(437, 545))
    background = PIL.Image.new(mode="RGBA", size=(381, 513), color=(50, 100, 150, 255))

    # creating background image from pfp
    pfp_scaled = pfp_original
    baseheight = 513
    hpercent = (baseheight/float(pfp_scaled.size[1]))
    wsize = int((float(pfp_scaled.size[0])*float(hpercent)))
    pfp_scaled = pfp_scaled.resize((baseheight,wsize), Image.Resampling.LANCZOS) # after this step pfp_scaled will be 513x513 square

    width, height = background_dimensions
    x_offset = (height - width) / 2
    top = 0
    bottom = height
    left = 0 + x_offset
    right = height - x_offset
    background = pfp_scaled.crop((left, top, right, bottom))

    # rounding background
    background_mask = Image.open('masks/background.png').convert('L')
    output = ImageOps.fit(background, background_mask.size, centering=(0.5, 0.5))
    output.putalpha(background_mask)
    background = output


    # creating blurry region on background
    x, y = blurry_background_offset
    cropped_img = background.crop((x, y, 369, 500))
    blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(10),).convert("RGBA")
    #blurred_img.putalpha(127)
    alpha_bg = PIL.Image.new(mode="RGBA", size=blurred_img.size, color=(18, 17, 21, 127))
    blurred_img = Image.alpha_composite(blurred_img, alpha_bg)

    background.paste(blurred_img, (x, y), create_rounded_rectangle_mask(cropped_img, radius))


    # creating pfp circle https://stackoverflow.com/a/22336005/11273040 and pasting it on background
    bigsize = (pfp_original.size[0] * 2, pfp_original.size[1] * 2)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp_circle_size, Image.Resampling.LANCZOS)

    pfp_circle = ImageOps.fit(pfp_original, mask.size, centering=(0.5, 0.5))
    pfp_circle.putalpha(mask)

    alpha_bg = PIL.Image.new(mode="RGBA", size=background.size, color=(0, 0, 0, 0))
    alpha_bg.paste(pfp_circle, pfp_circle_offset)

    background = Image.alpha_composite(background, alpha_bg)


    # creating server icon circle
    bigsize = (server_original.size[0] * 3, server_original.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(server_circle_size, Image.Resampling.LANCZOS)

    server_circle = ImageOps.fit(server_original, mask.size, centering=(0.5, 0.5))
    server_circle.putalpha(mask)

    server_circle_bg_size = (int(server_circle_size[0] * 1.07), int(server_circle_size[1] * 1.07))
    server_circle_bg = Image.open('masks/server_circle_background.png')
    server_circle_bg = server_circle_bg.resize(server_circle_bg_size)

    alpha_bg = PIL.Image.new(mode="RGBA", size=server_circle_bg_size, color=(0, 0, 0, 0))
    alpha_bg.paste(server_circle, ( int(server_circle_size[0]*0.07 / 2) , int(server_circle_size[1]*0.07 / 2)))
    server_circle = Image.alpha_composite(server_circle_bg, alpha_bg)

    mask = Image.open('masks/server_circle_opacity_mask.png').convert('L')
    mask = mask.resize(server_circle.size, Image.Resampling.LANCZOS)
    server_circle.putalpha(mask)

    alpha_bg = PIL.Image.new(mode="RGBA", size=background.size, color=(0, 0, 0, 0))
    alpha_bg.paste(server_circle, server_circle_offset)

    background = Image.alpha_composite(background, alpha_bg)

    # adding vet badge
    badge = Image.open('vet_badge.png')
    badge = badge.resize((30,30), Image.Resampling.LANCZOS)
    alpha_bg = PIL.Image.new(mode="RGBA", size=background.size, color=(0, 0, 0, 0))
    alpha_bg.paste(badge, (31, 439))
    alpha_bg.paste(badge, (68, 439))
    alpha_bg.paste(badge, (105, 439))
    alpha_bg.paste(badge, (142, 439))
    background = Image.alpha_composite(background, alpha_bg)

    #################
    # DRAWING TEXTS #
    #################
    # checking if nickname provided is longer than 9, if so then it needs to be cut and 3 dots need to be added
    if len(nickname) > 9:
        nickname = nickname[0:9] + "..."

    draw = ImageDraw.Draw(background)

    drawText(nickname, 32, (148, 45), 'ExtraBold', draw)
    drawText("#" + str(discriminator), 20, (148, 91), 'Regular', draw)
    drawText(str(labmem_number), 20, (230, 91), 'Regular', draw)
    drawText("|", 20, (216, 90), 'Regular', draw)
    drawText("Messages Sent", 20, (31, 247), 'Regular', draw)
    drawText("2036", 24, (31, 218), 'ExtraBold', draw)
    drawText("Badges accquired", 12, (31, 419), 'Bold', draw)
    drawText("Level", 12, (31, 279), 'Regular', draw)
    drawText("XP", 12, (31, 311), 'Regular', draw)
    drawText("Rank", 12, (31, 343), 'Regular', draw)
    drawText("Honor Points", 12, (31, 375), 'Regular', draw)

    # progress bar values (I don't use drawText, because it's simpler to handle anhors and aligns just this way)
    font = ImageFont.truetype("fonts/Nunito-VariableFont_wght.ttf", 12)
    font.set_variation_by_name('ExtraBold')
    draw.text((278, 279),"80",font=font, align="right", anchor="rt")
    draw.text((278, 311),"158K / 187K",font=font, align="right", anchor="rt")
    draw.text((278, 343),"#2",font=font, align="right", anchor="rt")
    draw.text((278, 375),"12K",font=font, align="right", anchor="rt")

    # DRAWING PROGRESS BARS
    progress_bar_level = createProgressBar(230, background.size, (31, 295))
    progress_bar_xp = createProgressBar(180, background.size, (31, 327))
    progress_bar_rank = createProgressBar(200, background.size, (31, 359))
    progress_bar_honorpoints = createProgressBar(160, background.size, (31, 391))
    background = Image.alpha_composite(background, progress_bar_level)
    background = Image.alpha_composite(background, progress_bar_xp)
    background = Image.alpha_composite(background, progress_bar_rank)
    background = Image.alpha_composite(background, progress_bar_honorpoints)


    # merging full_background (the one with alpha around it) with background (the one with all card contents in it)
    full_background.paste(background, background_offset, background)
    profile_card = full_background
    #profile_card.save("final_output.png")

    # converting final image to bytes (so it can be used to create discord file upload)
    bytes = BytesIO()
    profile_card.save(bytes, format="PNG")
    bytes.seek(0)

    return bytes
