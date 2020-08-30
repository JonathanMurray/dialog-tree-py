import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple

import pygame
from pygame.font import Font
from pygame.mixer import Sound
from pygame.surface import Surface

from config_file import load_dialog_from_file
from constants import BLACK, Millis
from dialog import DialogComponent
from graph import DialogGraph
from sound import SoundPlayer

FONT_DIR = "resources/fonts"
IMG_DIR = "resources/images"
SOUND_DIR = "resources/sounds"
DIALOG_DIR = "resources/dialog"

UI_MARGIN = 3
SCREEN_SIZE = 500, 500
PICTURE_SIZE = (SCREEN_SIZE[0] - UI_MARGIN * 2, 380)


class App:
    def __init__(self, screen: Surface, dialog_font: Font, choice_font: Font, images: Dict[str, Surface],
        animations: Dict[str, List[Surface]], sound_player: SoundPlayer, dialog_graph: DialogGraph):
        self._screen = screen
        self._dialog_component = DialogComponent(
            surface=Surface((SCREEN_SIZE[0] - UI_MARGIN * 2, SCREEN_SIZE[1] - UI_MARGIN * 2)),
            dialog_font=dialog_font,
            choice_font=choice_font,
            images=images,
            animations=animations,
            sound_player=sound_player,
            dialog_graph=dialog_graph,
            picture_size=PICTURE_SIZE,
            select_blip_sound_id="select_blip",
        )
        self._clock = pygame.time.Clock()

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._render()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _exit_game()

            if event.type == pygame.KEYDOWN:
                self._dialog_component.on_skip_text_button()
                if event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    self._dialog_component.on_delta_button(1)
                if event.key in [pygame.K_UP, pygame.K_LEFT]:
                    self._dialog_component.on_delta_button(-1)
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self._dialog_component.on_action_button()

    def _update(self):
        elapsed_time = Millis(self._clock.tick())
        self._dialog_component.update(elapsed_time)

    def _render(self):
        self._dialog_component.redraw()
        self._screen.fill(BLACK)
        self._screen.blit(self._dialog_component.surface, (UI_MARGIN, UI_MARGIN))
        pygame.display.update()


def start(dialog_filename: Optional[str] = None):
    pygame.init()
    dialog_font = Font(f"{FONT_DIR}/Monaco.dfont", 17)
    choice_font = Font(f"{FONT_DIR}/Monaco.dfont", 15)

    images, animations = load_images()
    sounds = load_sounds()
    sound_player = SoundPlayer(sounds, sounds["text_blip"])
    dialog_filename = dialog_filename or "wikipedia_example.json"
    dialog_graph = load_dialog_from_file(f"{DIALOG_DIR}/{dialog_filename}")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(dialog_graph.title or dialog_filename)
    app = App(screen, dialog_font, choice_font, images, animations, sound_player, dialog_graph)
    app.run()


def load_images() -> Tuple[Dict[str, Surface], Dict[str, List[Surface]]]:
    images: Dict[str, Surface] = {}
    animations: Dict[str, List[Surface]] = {}
    for filename in os.listdir(IMG_DIR):
        filepath = Path(IMG_DIR).joinpath(filename)
        if filepath.is_dir():
            frame_filenames = os.listdir(filepath)
            frame_filenames.sort()
            animations[filename] = [load_and_scale(filepath.joinpath(frame_filename))
                                    for frame_filename in frame_filenames]
        else:
            images[str(filename).split(".")[0]] = load_and_scale(filepath)
    print(f"Loaded {len(images) + sum((len(d) for d in animations.values()))} image files.")
    return images, animations


def load_sounds() -> Dict[str, Sound]:
    sounds: Dict[str, Sound] = {}
    for filename in os.listdir(SOUND_DIR):
        filepath = str(Path(SOUND_DIR).joinpath(filename))
        sound = load_sound_file(filepath)
        sound.set_volume(0.2)
        sounds[str(filename).split(".")[0]] = sound
    print(f"Loaded {len(sounds)} sound files.")
    return sounds


def load_sound_file(filepath: str):
    try:
        return Sound(filepath)
    except Exception as e:
        raise Exception(f"Failed to load sound file '{filepath}': {e}")


def load_and_scale(filepath: Path) -> Surface:
    try:
        # print(f"Loading image: {filepath}")
        surface = pygame.image.load(str(filepath))
        return pygame.transform.scale(surface, PICTURE_SIZE)
    except pygame.error as e:
        raise Exception(f"Failed to load image '{filepath}': {e}")


def _exit_game():
    print("Exiting.")
    pygame.quit()
    exit(0)
