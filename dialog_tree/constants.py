from typing import Tuple, NewType

FONT_DIR = "resources/fonts"
IMG_DIR = "resources/images"
SOUND_DIR = "resources/sounds"
DIALOG_DIR = "resources/dialog"

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 170, 200, 170

Vec2 = Tuple[int, int]
Vec3 = Tuple[int, int, int]

Millis = NewType("Millis", int)
