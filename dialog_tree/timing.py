from typing import Callable, Any

from constants import Millis


class PeriodicAction:
    def __init__(self, cooldown: Millis, callback: Callable[[], Any]):
        self._cooldown = cooldown
        self._callback = callback
        self._time_since_last_action = 0

    def update(self, elapsed_time: Millis):
        self._time_since_last_action += elapsed_time
        if self._time_since_last_action >= self._cooldown:
            self._time_since_last_action -= self._cooldown
            self._callback()
