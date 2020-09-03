import argparse
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
SOUND_DIR = "resources/sounds"

UI_MARGIN = 3
SCREEN_SIZE = 500, 500
PICTURE_SIZE = (SCREEN_SIZE[0] - UI_MARGIN * 2, 380)


class App:
    def __init__(self, screen: Surface, dialog_font: Font, choice_font: Font, images: Dict[str, Surface],
        animations: Dict[str, List[Surface]], sound_player: SoundPlayer, dialog_graph: DialogGraph,
        select_blip_sound_id: str):
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
            select_blip_sound_id=select_blip_sound_id,
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
                self._dialog_component.skip_text()
                if event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    self._dialog_component.move_choice_selection(1)
                if event.key in [pygame.K_UP, pygame.K_LEFT]:
                    self._dialog_component.move_choice_selection(-1)
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self._dialog_component.commit_selected_choice()

    def _update(self):
        elapsed_time = Millis(self._clock.tick())
        self._dialog_component.update(elapsed_time)

    def _render(self):
        self._dialog_component.redraw()
        self._screen.fill(BLACK)
        self._screen.blit(self._dialog_component.surface, (UI_MARGIN, UI_MARGIN))
        pygame.display.update()


def start(dialog_filepath: Optional[str] = None, image_dir: Optional[str] = None, sound_dir: Optional[str] = None):

    pygame.init()
    dialog_font = Font(f"{FONT_DIR}/Monaco.dfont", 17)
    choice_font = Font(f"{FONT_DIR}/Monaco.dfont", 15)

    dialog_graph = load_dialog_from_file(dialog_filepath)

    image_ids = []
    animation_ids = []
    if dialog_graph.background_image_id:
        image_ids.append(dialog_graph.background_image_id)
    for node in dialog_graph.nodes():
        graphics = node.graphics
        if graphics.image_ids:
            image_ids += graphics.image_ids
        if graphics.animation_id:
            animation_ids.append(graphics.animation_id)
    images, animations = load_images(image_dir, image_ids, animation_ids)

    text_blip_sound_id = "text_blip.ogg"
    select_blip_sound_id = "select_blip.ogg"
    sound_ids = [n.sound_id for n in dialog_graph.nodes() if n.sound_id is not None]
    sounds = load_sounds(sound_dir, sound_ids)
    sounds[text_blip_sound_id] = load_sound_file(str(Path(SOUND_DIR).joinpath(text_blip_sound_id)))
    sounds[select_blip_sound_id] = load_sound_file(str(Path(SOUND_DIR).joinpath(select_blip_sound_id)))

    sound_player = SoundPlayer(sounds, sounds[text_blip_sound_id])

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(dialog_graph.title or dialog_filepath)
    app = App(screen, dialog_font, choice_font, images, animations, sound_player, dialog_graph, select_blip_sound_id)
    app.run()


def load_images(directory: str, image_ids: List[str], animation_ids: List[str]) -> Tuple[
    Dict[str, Surface], Dict[str, List[Surface]]]:
    images: Dict[str, Surface] = {}
    animations: Dict[str, List[Surface]] = {}
    for filename in os.listdir(directory):
        filepath = Path(directory).joinpath(filename)
        if filepath.is_dir() and filename in animation_ids:
            frame_filenames = os.listdir(filepath)
            frame_filenames.sort()
            animations[filename] = [load_and_scale(filepath.joinpath(frame_filename))
                                    for frame_filename in frame_filenames]
        else:
            if filename in image_ids:
                images[filename] = load_and_scale(filepath)
    print(f"Loaded {len(images) + sum((len(d) for d in animations.values()))} image files.")
    return images, animations


def load_sounds(directory: str, sound_ids: List[str]) -> Dict[str, Sound]:
    sounds: Dict[str, Sound] = {}
    for filename in os.listdir(directory):
        if filename in sound_ids:
            filepath = str(Path(directory).joinpath(filename))
            sounds[filename] = load_sound_file(filepath)
    print(f"Loaded {len(sounds)} sound files.")
    return sounds


def load_sound_file(filepath: str):
    try:
        sound = Sound(filepath)
        sound.set_volume(0.2)
        return sound
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


def main():
    parser = argparse.ArgumentParser(description="Run a dialog from a JSON configuration file.")
    parser.add_argument("json_file", type=str, help="The JSON file.")
    parser.add_argument("--image_dir", type=str, help="The directory that we should look for image files in.")
    parser.add_argument("--sound_dir", type=str, help="The directory that we should look for sound files in.")

    args = vars(parser.parse_args())

    dialog_filepath = args.get("json_file", None)
    image_dir = args["image_dir"]
    sound_dir = args["sound_dir"]

    print("Starting application...")
    print(f"dialog filepath={dialog_filepath}")
    print(f"image dir={image_dir}")
    print(f"sound dir={sound_dir}")

    start(dialog_filepath=dialog_filepath, image_dir=image_dir, sound_dir=sound_dir)


if __name__ == '__main__':
    main()
