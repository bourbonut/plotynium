from ..types import T
from ..transformers import LegendPicker
from typing import TypeVar

TChannel = TypeVar("Channel", bound="Channel")

class Channel:

    def __init__(self, origin: T | None = None, picker: LegendPicker | None = None):
        self._origin = origin
        self._picker = picker
        self._is_valid = True

    def compare_and_update(self, channel: TChannel):
        self._is_valid = self._origin == channel._origin
        self._origin = channel._origin
        self._picker = channel._picker
