from typing import Tuple, NewType

import pygame

FONT_DIR = "resources/fonts"
IMG_DIR = "resources/images"
DIALOG_DIR = "resources/dialog"

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 170, 200, 170
EVENT_INTERVAL = pygame.USEREVENT + 1
Vec2 = Tuple[int, int]
Vec3 = Tuple[int, int, int]

Millis = NewType("Millis", int)
