from abc import ABC
from random import randint
from typing import Tuple, List, Optional, Dict

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from constants import WHITE, GREEN, BLACK, Vec2, Vec3, Millis
from graph import DialogNode
from sound import SoundPlayer
from text_util import layout_text_in_area
from timing import PeriodicAction


class Component(ABC):
    def __init__(self, surface: Surface):
        self.surface = surface

    def update(self, elapsed_time: Millis):
        pass


class ScreenShake:
    def __init__(self):
        self.x = 0
        self.y = 0
        self._remaining = 0

    def start(self, duration: Millis):
        self._remaining = duration

    def update(self, elapsed_time: Millis):
        self._remaining = max(0, self._remaining - elapsed_time)
        if self._remaining == 0:
            self.x, self.y = 0, 0
        else:
            self.x, self.y = randint(-10, 10), randint(-10, 10)


class Ui:
    def __init__(self, surface: Surface, picture_size: Vec2, dialog_node: DialogNode, dialog_font: Font,
        choice_font: Font, images: Dict[str, Surface], animations: Dict[str, List[Surface]], sound_player: SoundPlayer,
        background: Optional[Surface], select_blip_sound_id: str):
        self.surface = surface
        self._picture_size = picture_size
        self._width = surface.get_width()
        self._dialog_font = dialog_font
        self._choice_font = choice_font
        self._images = images
        self._animations = animations
        self._sound_player = sound_player
        self._background = background
        self._select_blip_sound_id = select_blip_sound_id

        # MUTABLE STATE BELOW
        self._dialog_node = dialog_node
        self._components: List[Tuple[Component, Vec2]] = []
        self._dialog_box = None
        self._choice_buttons = []
        self._active_choice_index = 0
        self._screen_shake = ScreenShake()

        self.set_dialog(dialog_node)

    def set_dialog(self, dialog_node: DialogNode):
        self._dialog_node = dialog_node

        graphics = dialog_node.graphics
        if graphics.image_ids:
            animation = Animation([self._images[i] for i in graphics.image_ids], graphics.offset)
        else:
            animation = Animation(self._animations[graphics.animation_id], graphics.offset)
        margin = 5
        dialog_box_size = (self._width - margin * 2, 120)
        if self._background:
            picture_size = (max(self._background.get_width(), animation.image().get_width()),
                            max(self._background.get_height(), animation.image().get_height()))
        else:
            picture_size = animation.image().get_size()
        self._components = [(Picture(Surface(picture_size), self._background, animation), (0, 0))]
        if dialog_node.text:
            self._dialog_box = TextBox(
                self._dialog_font, dialog_box_size, dialog_node.text,
                border_color=(150, 150, 150), text_color=(255, 255, 255), sound_player=self._sound_player)
            self._components.append(
                (self._dialog_box, (margin, self._picture_size[1] - dialog_box_size[1] - margin)))
            if dialog_node.graphics.instant_text:
                self._dialog_box.set_cursor_to_end()
        self._choice_buttons = []
        if graphics.screen_shake:
            self._screen_shake.start(graphics.screen_shake)

    def _add_choice_buttons(self):
        button_height = 40
        self._choice_buttons = [ChoiceButton(self._choice_font, (self._width, button_height), choice.text)
                                for choice in self._dialog_node.choices]
        self._active_choice_index = 0
        if self._choice_buttons:
            self._choice_buttons[self._active_choice_index].set_highlighted(True)
        for i, button in enumerate(self._choice_buttons):
            j = len(self._choice_buttons) - i
            position = (0, self.surface.get_height() - button_height * j - 5 * j)
            self._components.append((button, position))

    def redraw(self):
        self.surface.fill(BLACK)
        dx, dy = (self._screen_shake.x, self._screen_shake.y)
        for component, (x, y) in self._components:
            self.surface.blit(component.surface, (x + dx, y + dy))

    def update(self, elapsed_time: Millis):

        self._screen_shake.update(elapsed_time)

        for component, _ in self._components:
            component.update(elapsed_time)

        if self._dialog_box.is_cursor_at_end() and not self._choice_buttons:
            self._add_choice_buttons()

    def handle_delta_input(self, delta: int):
        if self._choice_buttons and len(self._choice_buttons) > 1:
            self._sound_player.play(self._select_blip_sound_id)
            self._choice_buttons[self._active_choice_index].set_highlighted(False)
            self._active_choice_index = (self._active_choice_index + delta) % len(self._choice_buttons)
            self._choice_buttons[self._active_choice_index].set_highlighted(True)

    def handle_action_input(self) -> Optional[int]:
        if self._choice_buttons:
            return self._active_choice_index

    def handle_skip_text_input(self):
        self._dialog_box.set_cursor_to_end()


class Animation:
    def __init__(self, frames: List[Surface], offset: Vec2):
        if not frames:
            raise ValueError("Cannot instantiate animation without frames!")
        self._frames = frames
        self._frame_index = 0
        self.offset = offset

    def change_frame(self):
        self._frame_index = (self._frame_index + 1) % len(self._frames)

    def image(self) -> Surface:
        return self._frames[self._frame_index]


class Picture(Component):

    def __init__(self, surface: Surface, background: Optional[Surface], animation: Animation):
        super().__init__(surface)
        self._background = background
        self._animation = animation
        self._redraw()
        self._periodic_frame_change = PeriodicAction(Millis(130), self._change_frame)

    def _redraw(self):
        self.surface.fill(BLACK)
        if self._background:
            self.surface.blit(self._background, (0, 0))
        self.surface.blit(self._animation.image(), self._animation.offset)

    def _change_frame(self):
        self._animation.change_frame()
        self._redraw()

    def update(self, elapsed_time: Millis):
        self._periodic_frame_change.update(elapsed_time)


class ChoiceButton(Component):
    def __init__(self, font: Font, size: Vec2, text: str, highlighted: bool = False):
        super().__init__(Surface(size))

        self._font = font
        self._text = text
        self._highlighted = highlighted
        self._container_rect = Rect((0, 0), size)

        self._redraw()

    def _redraw(self):
        self.surface.fill(BLACK)
        if self._highlighted:
            self.surface.fill((60, 60, 60), self._container_rect)
            pygame.draw.rect(self.surface, GREEN, self._container_rect, width=2, border_radius=4)
        else:
            pygame.draw.rect(self.surface, WHITE, self._container_rect, width=1, border_radius=4)
        rendered_text = self._font.render(self._text, True, WHITE)
        text_position = (self._container_rect.x + (self._container_rect.w - rendered_text.get_width()) // 2,
                         self._container_rect.y + (self._container_rect.h - rendered_text.get_height()) // 2)
        self.surface.blit(rendered_text, text_position)

    def set_highlighted(self, highlighted: bool):
        self._highlighted = highlighted
        self._redraw()


class TextBox(Component):
    def __init__(self, font: Font, size: Vec2, text: str, border_color: Vec3, text_color: Vec3,
        sound_player: SoundPlayer):
        super().__init__(Surface(size))
        self.surface.set_alpha(180)

        self._container_rect = Rect((0, 0), size)
        pad = 30
        self._text_area = self._container_rect.inflate(-pad, -pad)
        self._font = font
        self._border_color = border_color
        self._text_color = text_color
        self._sound_player = sound_player
        self._lines = self._split_into_lines(text)
        self._cursor = 0
        self._max_cursor_position = max(0, len(text) - 1)
        self._periodic_cursor_advance = PeriodicAction(Millis(40), self._advance_cursor)

        self._redraw()

    def _advance_cursor(self):
        if self._cursor < self._max_cursor_position:
            self._sound_player.play_text_blip()
            self._cursor += 1
            self._redraw()

    def update(self, elapsed_time: Millis):
        self._periodic_cursor_advance.update(elapsed_time)

    def set_cursor_to_end(self):
        self._cursor = self._max_cursor_position
        self._redraw()

    def is_cursor_at_end(self) -> bool:
        return self._cursor == self._max_cursor_position

    def _split_into_lines(self, text) -> List[str]:
        return list(layout_text_in_area(text, lambda t: self._font.size(t)[0], self._text_area.width))

    def _redraw(self):
        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, self._border_color, self._container_rect, width=1, border_radius=2)
        x, y = self._text_area.topleft
        num_chars_rendered = 0
        for line in self._lines:
            remaining = self._cursor + 1 - num_chars_rendered
            if remaining <= 0:
                return
            part_of_line = line[:remaining]
            rendered_line = self._font.render(part_of_line, True, self._text_color)
            self.surface.blit(rendered_line, (x, y))
            y += rendered_line.get_height()
            num_chars_rendered += len(part_of_line)
