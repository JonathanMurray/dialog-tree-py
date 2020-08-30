from typing import Dict, List

from pygame import Surface
from pygame.font import Font

from constants import Millis, Vec2
from graph import DialogGraph
from sound import SoundPlayer
from ui import Ui


class DialogComponent:

    def __init__(self, surface: Surface, dialog_font: Font, choice_font: Font, images: Dict[str, Surface],
        animations: Dict[str, List[Surface]], sound_player: SoundPlayer, dialog_graph: DialogGraph, picture_size: Vec2):
        self.surface = surface
        self._sound_player = sound_player
        self._dialog_graph = dialog_graph

        self._current_dialog_node = self._dialog_graph.current_node()

        background_id = self._dialog_graph.background_image_id
        background = images[background_id] if background_id else None
        self._ui = Ui(
            surface=surface,
            picture_size=picture_size,
            dialog_node=self._current_dialog_node,
            dialog_font=dialog_font,
            choice_font=choice_font,
            images=images,
            animations=animations,
            sound_player=sound_player,
            background=background,
        )
        self._play_dialog_sound()

    def update(self, elapsed_time: Millis):
        self._ui.update(elapsed_time)
        self._sound_player.update(elapsed_time)

    def on_delta_button(self, delta: int):
        self._ui.handle_delta_input(delta)

    def on_action_button(self):
        chosen_index = self._ui.handle_action_input()
        if chosen_index is not None:
            self._dialog_graph.make_choice(chosen_index)
            self._current_dialog_node = self._dialog_graph.current_node()
            self._play_dialog_sound()
            self._ui.set_dialog(self._current_dialog_node)

    def _play_dialog_sound(self):
        self._sound_player.stop_all_playing_sounds()
        if self._current_dialog_node.sound_id:
            self._sound_player.play(self._current_dialog_node.sound_id)

    def redraw(self):
        self._ui.redraw()
