import os

# Info
GAMEDIR = os.path.dirname(__file__)

# App Settings
WINDOW_NAME = "Cancer"
WINDOW_SIZE = (750,750)
FPS_LIMIT = 60

# Colours
COLOUR_WHITE = (255,255,255)
COLOUR_BLACK = (0,0,0)
COLOUR_RED = (255,0,0)
COLOUR_GREEN = (0,206,66)
COLOUR_BLUE = (0,49,206)
COLOUR_YELLOW = (255,255,0)

# Game Settings
BACKGROUND_COLOURS = [
    COLOUR_WHITE,
    COLOUR_RED,
    COLOUR_GREEN,
    COLOUR_BLUE,
    COLOUR_YELLOW,
    ]
SPRITE_PATH = os.path.join(GAMEDIR, "assets", "spinner_new.tif")
MUSIC_PATH = os.path.join(GAMEDIR, "assets", "music")
