from typing import Dict

import pygame.mixer
from pygame.mixer import Sound, Channel

from constants import Millis
from timing import PeriodicAction

SOUND_EFFECTS = 1


class SoundPlayer:
    def __init__(self, sounds: Dict[str, Sound]):
        self._sounds = sounds
        self._blip_channel = Channel(SOUND_EFFECTS)
        self._periodic_text_blip = PeriodicAction(Millis(75), self._play_queued_text_blip)
        self._text_blip_queued = False

    def update(self, elapsed_time: Millis):
        self._periodic_text_blip.update(elapsed_time)

    def _play_queued_text_blip(self):
        if self._text_blip_queued:
            self._text_blip_queued = False
            self.play("text_blip")

    def play(self, sound_id: str):
        sound = self._sounds[sound_id]
        sound.play()

    def play_text_blip(self):
        # We do it this way to avoid excessive spam of this sound effect (which sounds bad)
        self._text_blip_queued = True

    @staticmethod
    def stop_all_playing_sounds():
        pygame.mixer.fadeout(250)
