from dataclasses import dataclass
from math import sqrt

__all__ = [
    "CanvasProperties",
    "DEFAULT_LEGEND_HEIGHT",
    "DEFAULT_LEGEND_WIDTH",
    "DEFAULT_CANVAS_WIDTH",
    "LegendProperties",
    "Margin",
]

DEFAULT_CANVAS_WIDTH = 640 # without legend
DEFAULT_LEGEND_WIDTH = 240
DEFAULT_LEGEND_HEIGHT = 50

@dataclass
class Margin:
    top: int
    left: int
    bottom: int
    right: int


class Properties:
    def __init__(self, width: int, height: int, margin: Margin):
        self._width = width
        self._height = height
        self._margin = margin

    def set_width(self, width: int):
        self._width = width
        
    def set_height(self, height: int):
        self._height = height

    def set_margin(self, margin: Margin):
        self._margin = margin


class CanvasProperties(Properties):
    def __init__(self):
        super().__init__(
            DEFAULT_CANVAS_WIDTH,
            int(DEFAULT_CANVAS_WIDTH / sqrt(2)),
            Margin(0, 0, 0, 0),
        )


class LegendProperties(Properties):
    def __init__(self):
        super().__init__(
            DEFAULT_LEGEND_WIDTH,
            DEFAULT_LEGEND_HEIGHT,
            Margin(0, 0, 0, 0),
        )
