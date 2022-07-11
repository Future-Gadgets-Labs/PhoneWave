import sys
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageEnhance, ImageFilter
import requests

from app.utilities import text
from .. import utils
from . import constants


def draw_profile_card(
    avatar_url,
    nickname,
    discriminator,
    labmem_number,
    level,
    rank,
    messages_sent,
    xp_current,
    next_level_xp,
    badges_list,
):
    """
    creates profile card image with provided data, and returns it in form of BytesIO bytes

    avatar_url (string): Link to image, that will be used as both card background and avatar circle
    nickname (string): Nickname that will be used for the card. If it's too long it will be trimmed (see app.utilities.text.trim_with_ellipsis)
    discriminator (int | string): Discord 4 digits long discriminator
    labmem_number (int): Lab member number, usually 3 digits long
    level (int): Discord level
    rank (int): Discord rank
    messages_sent (int): number of messages sent
    xp_current (int): current amount of user's exp
    next_level_xp (int): amount of xp needed to hit next level
    badges_list (array of strings): Each string represents one badge, that user got. There's predefined list of badges at drawing/profilecard/constants.py.
    """

    # getting base images
    pfp_original = Image.open(requests.get(avatar_url, stream=True).raw)
    background = Image.new(
        mode="RGBA", size=constants.BACKGROUND_DIMENSIONS, color=(0, 0, 0, 255)
    )

    pfp_scaled = ImageOps.fit(pfp_original, constants.BACKGROUND_DIMENSIONS)
    # putting scaled pfp on background
    background = pfp_scaled.crop(
        (0, 0, constants.BACKGROUND_DIMENSIONS[0], constants.BACKGROUND_DIMENSIONS[1])
    )

    # making background rounded rectangle (according to masks/background.png)
    background = utils.apply_alpha_with_mask(background, constants.BACKGROUND_MASK_PATH)

    # adding blurry region in the middle of background
    cropped_img = background.crop(
        (
            constants.BLURRY_BACKGROUND_OFFSET[0],
            constants.BLURRY_BACKGROUND_OFFSET[1],
            constants.BLURRY_REGION_SIZE[0] + constants.BLURRY_BACKGROUND_OFFSET[0],
            constants.BLURRY_REGION_SIZE[1] + constants.BLURRY_BACKGROUND_OFFSET[1],
        )
    )

    blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(25)).convert("RGBA")
    alpha_bg = Image.new(mode="RGBA", size=blurred_img.size, color=(18, 17, 21, 127))
    blurred_img = Image.alpha_composite(blurred_img, alpha_bg)

    background.paste(
        blurred_img,
        (constants.BLURRY_BACKGROUND_OFFSET[0], constants.BLURRY_BACKGROUND_OFFSET[1]),
        utils.create_rounded_rectangle_mask(
            blurred_img, constants.BLURRY_REGION_RADIUS
        ),
    )

    # adding semi-black-transparent rounded rectangle areas on top of blurried area
    background = utils.create_semi_transparent_black_region_on_background(
        constants.BLACK_REGION_1_SIZE, constants.BLACK_REGION_1_OFFSET, background
    )
    background = utils.create_semi_transparent_black_region_on_background(
        constants.BLACK_REGION_2_SIZE, constants.BLACK_REGION_2_OFFSET, background
    )

    for i in range(0, 7):
        additional_x_offset = i * constants.BADGES_SPACING + i * constants.BADGE_SIZE[0]
        badge_offset = (
            constants.FIRST_BADGE_OFFSET[0] + additional_x_offset,
            constants.FIRST_BADGE_OFFSET[1],
        )
        if i < len(badges_list):
            background = utils.draw_badge_image_on_background(
                badge_offset, background, badges_list[i]
            )
        else:
            background = utils.draw_badge_background_on_background(
                badge_offset, background
            )

    # creating pfp circle https://stackoverflow.com/a/22336005/11273040 and pasting it on background
    bigsize = (pfp_original.size[0] * 2, pfp_original.size[1] * 2)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)

    mask = mask.resize(constants.PFP_CIRCLE_SIZE, Image.Resampling.LANCZOS)
    pfp_circle = ImageOps.fit(pfp_original, mask.size, centering=(0.5, 0.5))
    pfp_circle.putalpha(mask)

    alpha_bg = Image.new(mode="RGBA", size=background.size, color=(0, 0, 0, 0))
    alpha_bg.paste(pfp_circle, constants.PFP_CIRCLE_OFFSET)
    background = Image.alpha_composite(background, alpha_bg)

    # progress bar
    progress_bar_xp = utils.create_progress_bar(
        87, constants.XP_BAR_SIZE, background.size, constants.XP_BAR_OFFSET
    )
    background = Image.alpha_composite(background, progress_bar_xp)

    # drawing texts
    draw = ImageDraw.Draw(background)

    utils.draw_text(
        text.trim_with_ellipsis(nickname, 12), 32, (24, 56), "ExtraBold", draw
    )
    utils.draw_text(
        str(discriminator) + "  |  " + str(labmem_number), 20, (24, 96), "Regular", draw
    )

    utils.draw_text("LEVEL", 16, (40, 198), "Regular", draw)
    utils.draw_text(str(level), 20, (50, 222), "ExtraBold", draw)
    utils.draw_text("XP", 12, (100, 176), "Regular", draw)
    utils.draw_text("Level", 12, (100, 217), "Regular", draw)
    utils.draw_text("Rank", 12, (100, 236), "Regular", draw)
    utils.draw_text("Messages Sent", 12, (100, 255), "Regular", draw)
    utils.draw_text("Badges Acquired", 12, (36, 304), "Regular", draw)

    # making number more human friendly
    messages_sent = text.shorten_big_number(messages_sent)
    xp_current = text.shorten_big_number(xp_current)
    next_level_xp = text.shorten_big_number(next_level_xp)

    # progress bar values (I don't use utils.draw_text(), because it's simpler to handle anhors and aligns just this way)
    font = ImageFont.truetype(constants.DEFAULT_FONT_PATH, 12)
    font.set_variation_by_name("ExtraBold")
    draw.text(
        (380, 178),
        xp_current + " / " + next_level_xp,
        font=font,
        align="right",
        anchor="rt",
    )
    draw.text((380, 219), "89", font=font, align="right", anchor="rt")
    draw.text((380, 238), "#2", font=font, align="right", anchor="rt")
    draw.text((380, 257), messages_sent, font=font, align="right", anchor="rt")
    draw.text(
        (380, 306), str(len(badges_list)) + "/7", font=font, align="right", anchor="rt"
    )

    # this is final image
    profile_card = background

    # transforming it into bytes, so it can be used for discord file
    bytes = BytesIO()
    profile_card.save(bytes, format="PNG")
    bytes.seek(0)

    return bytes
