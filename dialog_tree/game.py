import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple

import pygame
from pygame.font import Font
from pygame.mixer import Sound
from pygame.surface import Surface

from constants import BLACK, FONT_DIR, EVENT_INTERVAL, IMG_DIR, DIALOG_DIR, Millis, SOUND_DIR
from dialog_config_file import load_dialog_from_file
from dialog_graph import Dialog
from ui import Ui

UI_MARGIN = 3
SCREEN_SIZE = 500, 500
PICTURE_SIZE = (SCREEN_SIZE[0] - UI_MARGIN * 2, 380)


class Game:

    def __init__(self, screen: Surface, dialog_font: Font, choice_font: Font, images: Dict[str, Surface],
        animations: Dict[str, List[Surface]], sounds: Dict[str, Sound], dialog_graph: Dialog):
        self._screen = screen
        self._sounds = sounds
        self._dialog_graph = dialog_graph

        self._clock = pygame.time.Clock()

        self._current_dialog_node = self._dialog_graph.current_node()

        ui_size = (screen.get_width() - UI_MARGIN * 2, screen.get_height() - UI_MARGIN * 2)
        background_id = self._dialog_graph.background_image_id
        background = images[background_id] if background_id else None
        self._ui = Ui(
            surface=Surface(ui_size),
            picture_size=PICTURE_SIZE,
            dialog_node=self._current_dialog_node,
            dialog_font=dialog_font,
            choice_font=choice_font,
            images=images,
            animations=animations,
            text_blip_sound=sounds["text_blip"],
            select_blip_sound=sounds["select_blip"],
            background=background,
        )

    def run(self):
        while True:
            self._update()
            self._render()

    def _update(self):

        elapsed_time = Millis(self._clock.tick())

        self._ui.update(elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _exit_game()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    self._ui.try_change_active_choice(1)
                if event.key in [pygame.K_UP, pygame.K_LEFT]:
                    self._ui.try_change_active_choice(-1)
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self._make_choice()

    def _make_choice(self):
        chosen_index = self._ui.try_make_choice()
        if chosen_index is not None:
            self._dialog_graph.make_choice(chosen_index)
            self._current_dialog_node = self._dialog_graph.current_node()
            if self._current_dialog_node.sound_id:
                # TODO stop any currently playing sound effect when going to new screen
                self._sounds[self._current_dialog_node.sound_id].play()
            self._ui.set_dialog(self._current_dialog_node)

    def _render(self):
        self._screen.fill(BLACK)
        self._ui.redraw()
        self._screen.blit(self._ui.surface, (UI_MARGIN, UI_MARGIN))
        pygame.display.update()


def start(dialog_filename: Optional[str] = None):
    pygame.init()
    dialog_font = Font(f"{FONT_DIR}/Monaco.dfont", 17)
    choice_font = Font(f"{FONT_DIR}/Monaco.dfont", 15)

    pygame.display.init()
    pygame.time.set_timer(EVENT_INTERVAL, 40)

    images, animations = load_images()
    sounds = load_sounds()
    dialog_filename = dialog_filename or "wikipedia_example.json"
    dialog_graph = load_dialog_from_file(f"{DIALOG_DIR}/{dialog_filename}")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(dialog_graph.title or dialog_filename)
    game = Game(screen, dialog_font, choice_font, images, animations, sounds, dialog_graph)
    game.run()


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
