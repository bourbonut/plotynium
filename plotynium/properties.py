from dataclasses import dataclass
from math import sqrt
from typing import TypeVar

__all__ = [
    "CanvasProperties",
    "DEFAULT_LEGEND_HEIGHT",
    "DEFAULT_LEGEND_WIDTH",
    "DEFAULT_CANVAS_WIDTH",
    "DEFAULT_SQUARE_SIZE",
    "DEFAULT_SYMBOL_SIZE",
    "LegendProperties",
    "Margin",
]

TLegendProperties = TypeVar("LegendProperties", bound="LegendProperties")

DEFAULT_CANVAS_WIDTH = 640 # without legend
DEFAULT_LEGEND_WIDTH = 240
DEFAULT_LEGEND_HEIGHT = 50
DEFAULT_SQUARE_SIZE = 15
DEFAULT_SYMBOL_SIZE = 5

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

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def margin(self) -> Margin:
        return self._margin


class CanvasProperties(Properties):
    def __init__(self):
        super().__init__(
            DEFAULT_CANVAS_WIDTH,
            int(DEFAULT_CANVAS_WIDTH / sqrt(2)),
            Margin(0, 0, 0, 0),
        )
        self._translate_x = 0
        self._translate_y = 0

    def set_translate(self, x: int = 0, y: int = 0):
        self._translate_x = x
        self._translate_y = y

    @property
    def translate(self) -> str | None:
        return (
            f"translate({self._translate_x}, {self._translate_y})"
            if self._translate_x != 0 or self._translate_y != 0
            else None
        )


class LegendProperties(Properties):
    def __init__(self):
        super().__init__(
            DEFAULT_LEGEND_WIDTH,
            DEFAULT_LEGEND_HEIGHT,
            Margin(
                (DEFAULT_LEGEND_HEIGHT - DEFAULT_SQUARE_SIZE // 2) // 2,
                DEFAULT_SQUARE_SIZE,
                (DEFAULT_LEGEND_HEIGHT - DEFAULT_SQUARE_SIZE // 2) // 2,
                DEFAULT_SQUARE_SIZE
            ),
        )

    @classmethod
    def new(
        self,
        width: int | None = None,
        height: int | None = None,
        margin_top: int = 0,
        margin_left: int = 0,
        margin_bottom: int = 0,
        margin_right: int = 0,
    ) -> TLegendProperties:
        properties = LegendProperties()
        if width is not None:
            properties.set_width(width)
        if height is not None:
            properties.set_height(height)
        properties.set_margin(
            Margin(
                margin_top,
                margin_left,
                margin_bottom,
                margin_right,
            )
        )
        return properties
