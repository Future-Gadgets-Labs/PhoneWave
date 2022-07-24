from pathlib import Path

# CONSTANTS THAT ARE USED FOR drawing/
# THEY DEFINE PLACEMENTS/COLORS AND DEFAULT FONTS/IMAGES PATHS


# SIZES
BACKGROUND_DIMENSIONS = (419, 404)
BLURRY_REGION_RADIUS = 12
BLURRY_REGION_SIZE = (395, 380)
BLACK_REGION_1_SIZE = (371, 118)
BLACK_REGION_2_SIZE = (371, 88)
BADGE_SIZE = (41, 41)
PFP_CIRCLE_SIZE = (100, 100)
XP_BAR_SIZE = (283, 10)


# OFFSETS
BLURRY_BACKGROUND_OFFSET = (12, 12)
BLACK_REGION_1_OFFSET = (24, 164)
BLACK_REGION_2_OFFSET = (24, 292)
FIRST_BADGE_OFFSET = (36, 329)
BADGES_SPACING = 10
PFP_CIRCLE_OFFSET = (295, 39)
XP_BAR_OFFSET = (100, 195)

# COLORS

# PATHS
p = Path(__file__).resolve().parent
ASSETS_PATH = p.parent.parent.parent / "assets"
MASKS_PATH = ASSETS_PATH / "masks"

BACKGROUND_MASK_PATH = MASKS_PATH / "profile_card_background.png"
PROGRESS_BAR_BACKGROUND_PATH = MASKS_PATH / "progressbar_background.png"
PROGRESS_BAR_FULL_PATH = MASKS_PATH / "progressbar_full.png"
PROGRESS_BAR_MASK_PATH = MASKS_PATH / "progressbar_mask.png"

default_discord_pfp = ASSETS_PATH / "others/default_discord_pfp.png"

BADGES_MAP = {
    "operation_elysian_veteran": str(ASSETS_PATH / "badges/operation_elysian_vet.png"),
    "daru69": str(ASSETS_PATH / "badges/daru69.png"),
}

# FONTS
DEFAULT_FONT_PATH = str(
    ASSETS_PATH / "fonts/MerriweatherSansItalic/MerriweatherSans-VariableFont_wght.ttf"
)
