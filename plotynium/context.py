from dataclasses import dataclass
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions
from detroit.types import Scaler

__all__ = ["Context"]

@dataclass
class Margin:
    top: int
    left: int
    bottom: int
    right: int

class Context:
    def __init__(
        self,
        width: int,
        height: int,
        margin: Margin,
        x_options: XOptions,
        y_options: YOptions,
        color_options: ColorOptions,
        style_options: StyleOptions,
        symbol_options: SymbolOptions,
        x_scale: Scaler,
        y_scale: Scaler,
        x_label: str | None = None,
        y_label: str | None = None,
    ):
        self._width = width
        self._height = height
        self._margin = margin

        self._x_options = x_options
        self._y_options = y_options
        self._color_options = color_options
        self._style_options = style_options
        self._symbol_options = symbol_options

        self._color_labels = []
        self._symbol_options = []

        self._x = x_scale
        self._y = y_scale

    @property
    def x_label(self):
        return self._x_label

    @property
    def y_label(self):
        return self._y_label

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def color(self):
        return self._style_options.color

    @property
    def font_size(self):
        return self._style_options.font_size

    @property
    def font_family(self):
        return self._style_options.font_family

    @property
    def background(self):
        return self._style_options.background
