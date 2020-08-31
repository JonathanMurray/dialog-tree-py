from typing import Dict, List

from pygame import Surface
from pygame.font import Font

from constants import Millis, Vec2
from graph import DialogGraph
from sound import SoundPlayer
from ui import Ui


class DialogComponent:

    def __init__(self, surface: Surface, dialog_font: Font, choice_font: Font, images: Dict[str, Surface],
        animations: Dict[str, List[Surface]], sound_player: SoundPlayer, dialog_graph: DialogGraph, picture_size: Vec2,
        select_blip_sound_id: str):
        self._validate_inputs(dialog_graph, images)
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
            select_blip_sound_id=select_blip_sound_id
        )
        self._play_dialog_sound()

    @staticmethod
    def _validate_inputs(dialog_graph: DialogGraph, images: Dict[str, Surface]):
        for node in dialog_graph.nodes():
            if node.graphics.image_ids:
                for image_id in node.graphics.image_ids:
                    if image_id not in images:
                        raise ValueError(
                            f"Invalid config! Graph node '{node.node_id}' refers to missing image: '{image_id}'")
        background_id = dialog_graph.background_image_id
        if background_id and background_id not in images:
            raise ValueError(f"Invalid config! Graph refers to missing background image: '{background_id}'")

    def update(self, elapsed_time: Millis):
        self._ui.update(elapsed_time)
        self._sound_player.update(elapsed_time)

    def skip_text(self):
        self._ui.skip_text()

    def move_choice_selection(self, delta: int):
        self._ui.move_choice_highlight(delta)

    def select_choice_at_position(self, ui_coordinates: Vec2):
        chosen_index = self._ui.choice_button_at_position(ui_coordinates)
        if chosen_index is not None:
            self._ui.set_highlighted_choice(chosen_index)

    def commit_selected_choice(self):
        chosen_index = self._ui.highlighted_choice()
        if chosen_index is not None:
            self._commit_choice(chosen_index)

    def commit_choice_at_position(self, ui_coordinates: Vec2):
        chosen_index = self._ui.choice_button_at_position(ui_coordinates)
        if chosen_index is not None:
            self._commit_choice(chosen_index)

    def _commit_choice(self, chosen_index: int):
        self._dialog_graph.make_choice(chosen_index)
        self._current_dialog_node = self._dialog_graph.current_node()
        self._play_dialog_sound()
        self._ui.set_dialog(self._current_dialog_node)

    def current_node_id(self) -> str:
        return self._current_dialog_node.node_id

    def _play_dialog_sound(self):
        self._sound_player.stop_all_playing_sounds()
        if self._current_dialog_node.sound_id:
            self._sound_player.play(self._current_dialog_node.sound_id)

    def redraw(self):
        self._ui.redraw()
