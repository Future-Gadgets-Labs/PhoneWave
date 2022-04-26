import sys
import PIL
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageEnhance, ImageFilter
import constants
solid_fill =  (50,50,50,255)

def drawBadgeBackgroundOnBackground(offset, background):
    black_region = PIL.Image.new(mode="RGBA", size=constants.badge_size, color=(255, 255, 255, 25))
    background.paste(black_region, (offset[0], offset[1]), create_rounded_rectangle_mask(black_region, 8))
    return background

def drawBadgeImageOnBackground(offset, background, badge_name):
    badge_path = constants.badges_map[badge_name]
    black_region = Image.open(badge_path)
    black_region = black_region.resize(constants.badge_size, Image.Resampling.LANCZOS)
    background.paste(black_region, (offset[0], offset[1]), create_rounded_rectangle_mask(black_region, 8))
    return background

def createSemiTransparentBlackRegionOnBackground(size, offset, background):
    cropped_img = background.crop((
        offset[0],
        offset[1],
        size[0]+offset[0],
        size[1]+offset[1]
    ))
    alpha_bg = PIL.Image.new(mode="RGBA", size=cropped_img.size, color=(18, 17, 21, 127))
    black_region = Image.alpha_composite(cropped_img, alpha_bg)
    background.paste(black_region, (offset[0], offset[1]), create_rounded_rectangle_mask(black_region, 12))
    return background

def applyAlphaWithMask(image, mask_path):
    mask = Image.open(mask_path).convert('L')
    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

def drawText(text, size, location, weight, draw, color=(255,255,255)):
    font_path = constants.default_font
    font = ImageFont.truetype(font_path, size)
    font.set_variation_by_name(weight)
    draw.text(location, text, color, font=font)

def create_rounded_rectangle_mask(rectangle, radius):
    # create mask image. all pixels set to translucent
    i = Image.new("RGBA",rectangle.size,(0,0,0,0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill = solid_fill)

    # max_x, max_y
    mx,my = rectangle.size

    # paste corner rotated as needed
    # use corners alpha channel as mask

    i.paste(corner, (0, 0), corner)
    i.paste(corner.rotate(90), (0, my - radius),corner.rotate(90))
    i.paste(corner.rotate(180), (mx - radius,   my - radius),corner.rotate(180))
    i.paste(corner.rotate(270), (mx - radius, 0),corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(i)
    draw.rectangle( [(radius,0),(mx-radius,my)],fill=solid_fill)
    draw.rectangle( [(0,radius),(mx,my-radius)],fill=solid_fill)

    return i

def ReduceOpacity(im, opacity):
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def createProgressBar(progress_percent, target_size, background_size, location):

    # getting how much progress user has
    scale =  target_size[0] / 100
    target_progressbar_width = int(scale * progress_percent)


    # setting progressbar_background
    progressbar_background = Image.open('masks/progressbar_background.png')
    progressbar_background = progressbar_background.resize((target_size[0], target_size[1]), Image.Resampling.LANCZOS)
    alpha_bg = PIL.Image.new(mode="RGBA", size=progressbar_background.size, color=(0, 0, 0, 0))
    alpha_bg.paste(progressbar_background, (0, 0))

    # getting progressbar_full and rounding it to mask
    progressbar_full = Image.open('masks/progressbar_full.png')
    progressbar_full = progressbar_full.convert('RGBA')
    progressbar_full = progressbar_full.resize((target_size[0],target_size[1]), Image.Resampling.LANCZOS)

    progressbar_mask = Image.open('masks/progressbar_mask.png').convert('L')
    progressbar_mask = progressbar_mask.resize((target_size[0],target_size[1]), Image.Resampling.LANCZOS)
    output = ImageOps.fit(progressbar_full, progressbar_mask.size, centering=(0.5, 0.5))
    output.putalpha(progressbar_mask)
    progressbar_full = output

    alpha_rectangle = PIL.Image.new(mode="RGBA", size=(target_size[0]-target_progressbar_width, target_size[1]), color=(0, 0, 0, 0))
    progressbar_full.paste(alpha_rectangle, (target_progressbar_width, 0))

    # creating head for gradient
    progressbar_mask_head = progressbar_mask.crop((target_size[0]-target_size[1], 0, target_size[0], target_size[1]))
    progressbar_head = progressbar_full.crop((target_progressbar_width-target_size[1], 0, target_progressbar_width, target_size[1]))
    output = ImageOps.fit(progressbar_head, progressbar_mask_head.size, centering=(0.5, 0.5))
    output.putalpha(progressbar_mask_head)
    progressbar_head = output

    progressbar_full.paste(progressbar_head, (target_progressbar_width-target_size[1], 0))

    alpha_bg = Image.alpha_composite(alpha_bg, progressbar_full)
    alpha_bg_bg = PIL.Image.new(mode="RGBA", size=background_size, color=(0, 0, 0, 0))
    alpha_bg_bg.paste(alpha_bg, location)

    return alpha_bg_bg
