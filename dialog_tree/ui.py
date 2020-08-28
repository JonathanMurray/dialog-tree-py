from abc import ABC
from typing import Iterator, Tuple, Callable, List

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from constants import WHITE, GREEN, BLACK, Vec2, Vec3


class Component(ABC):
    def __init__(self, surface: Surface):
        self.surface = surface


class ComponentCollection:
    def __init__(self, components: List[Tuple[Component, Vec2]]):
        self.components = components

    def render(self, screen: Surface):
        for component, position in self.components:
            screen.blit(component.surface, position)


class Portrait(Component):
    def __init__(self, image: Surface):
        super().__init__(image)


class Button(Component):
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
    def __init__(self, font: Font, size: Vec2, text: str, border_color: Vec3, text_color: Vec3):
        super().__init__(Surface(size))

        self._container_rect = Rect((0, 0), size)
        pad = 30
        self._text_area = self._container_rect.inflate(-pad, -pad)
        self._font = font
        self._border_color = border_color
        self._text_color = text_color
        self._lines = self._split_into_lines(text)
        self._cursor = 0
        self._max_cursor_position = len(text) - 1

        self._redraw()

    def advance_cursor(self) -> bool:
        """Advance the cursor one step, and return True if this made it reach the end"""
        if self._cursor == self._max_cursor_position:
            return False

        self._cursor = min(self._cursor + 1, self._max_cursor_position)
        self._redraw()
        return self._cursor == self._max_cursor_position

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


def layout_text_in_area(text: str, font_width: Callable[[str], int], width: int) -> Iterator[str]:
    start = 0
    end = 0

    while True:

        if text[start] == ' ':
            # Our line is starting with whitespace --> advance forward to skip whitespace
            for i in range(start + 1, len(text) + 1):
                if text[i] != ' ':
                    start = i
                    break

        if end >= len(text):
            # We have reached the end of the string --> we're done
            yield text[start:]
            return
        substr = text[start:end + 1]
        overflow = font_width(substr) > width
        if overflow:
            # we have a substring [start->end] that is wider than allowed
            if text[end] == ' ':
                # we are at a word-boundary so we can return all previous text
                yield text[start:end]
                start = end
            else:
                # mid-word --> we need to go back left to find a word-boundary to wrap line at
                found = False
                for i in range(end - 1, start, -1):
                    if text[i] == ' ':
                        # we found a word boundary --> yield line and go on with main loop
                        yield text[start:i + 1]
                        start = end = i + 1
                        found = True
                        break
                if not found:
                    # failed to find a word-boundary --> resort to returning mid-word
                    yield text[start:end]
                    start = end
        else:
            end += 1
