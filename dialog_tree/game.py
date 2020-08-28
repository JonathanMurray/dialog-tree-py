import os
from typing import Dict, Optional

import pygame
from pygame.font import Font
from pygame.surface import Surface

from constants import BLACK, FONT_DIR, EVENT_INTERVAL, IMG_DIR, DIALOG_DIR
from dialog_config_file import load_dialog_from_file
from dialog_graph import DialogGraph
from ui import TextBox, Button, ComponentCollection, Portrait

PORTRAIT_IMAGE_SIZE = (480, 240)


class Game:
    def __init__(self, screen: Surface, dialog_font: Font, choice_font: Font, images: Dict[str, Surface],
        dialog_graph: DialogGraph):
        self._screen = screen
        self._dialog_font = dialog_font
        self._choice_font = choice_font
        self._images = images
        self._dialog_graph = dialog_graph

        text, self._active_image_id, self._choice_texts = self._dialog_graph.get_current_state()

        self._setup_ui_with_dialog(text)

    def _setup_ui_with_dialog(self, dialog_text: str):
        margin = 10
        inner_width = self._screen.get_width() - margin * 2
        self._dialog_box = TextBox(self._dialog_font, (inner_width, 120), dialog_text,
                                   border_color=(150, 150, 150), text_color=(255, 255, 255))

        components = [
            (Portrait(self._images[self._active_image_id]), (margin, margin)),
            (self._dialog_box, (margin, PORTRAIT_IMAGE_SIZE[1] + margin * 2)),
        ]
        self._ui = ComponentCollection(components)
        self._choice_buttons = []

    def _add_buttons_to_ui(self):
        margin = 10
        inner_width = self._screen.get_width() - margin * 2

        button_height = 40
        self._choice_buttons = [Button(self._choice_font, (inner_width, button_height), choice_text)
                                for choice_text in self._choice_texts]
        self._active_choice_index = 0
        if self._choice_buttons:
            self._choice_buttons[self._active_choice_index].set_highlighted(True)
        for i, button in enumerate(self._choice_buttons):
            j = len(self._choice_buttons) - i
            position = (margin, self._screen.get_height() - button_height * j - margin * j)
            self._ui.components.append((button, position))

    def run(self):
        while True:
            self._handle_events()
            self._render()

    def _handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                _exit_game()
            if event.type == EVENT_INTERVAL:
                reached_end = self._dialog_box.advance_cursor()
                if reached_end:
                    self._add_buttons_to_ui()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    self._change_active_choice(1)
                if event.key in [pygame.K_UP, pygame.K_LEFT]:
                    self._change_active_choice(-1)
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self._make_choice()

    def _change_active_choice(self, delta: int):
        if self._choice_buttons:
            self._choice_buttons[self._active_choice_index].set_highlighted(False)
            self._active_choice_index = (self._active_choice_index + delta) % len(self._choice_buttons)
            self._choice_buttons[self._active_choice_index].set_highlighted(True)

    def _make_choice(self):
        if self._choice_buttons:
            self._dialog_graph.make_choice(self._active_choice_index)
            dialog_text, self._active_image_id, self._choice_texts = self._dialog_graph.get_current_state()
            self._setup_ui_with_dialog(dialog_text)

    def _render(self):
        self._screen.fill(BLACK)
        self._ui.render(self._screen)
        pygame.display.update()


def start(dialog_filename: Optional[str] = None):
    pygame.init()
    dialog_font = Font(f"{FONT_DIR}/Monaco.dfont", 17)
    choice_font = Font(f"{FONT_DIR}/Monaco.dfont", 15)

    pygame.display.init()
    pygame.time.set_timer(EVENT_INTERVAL, 40)

    image_paths = os.listdir(IMG_DIR)
    images = {path.split(".")[0]: load_image(path) for path in image_paths}

    dialog_filename = dialog_filename or "wikipedia_example.json"
    dialog_graph = load_dialog_from_file(f"{DIALOG_DIR}/{dialog_filename}")

    screen_size = 500, 500
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(dialog_graph.title or dialog_filename)
    game = Game(screen, dialog_font, choice_font, images, dialog_graph)
    game.run()


def load_image(filename: str):
    print(f"Loading image: {filename}")
    return pygame.transform.scale(pygame.image.load(f"{IMG_DIR}/{filename}"), PORTRAIT_IMAGE_SIZE)


def _exit_game():
    print("Exiting.")
    pygame.quit()
    exit(0)
