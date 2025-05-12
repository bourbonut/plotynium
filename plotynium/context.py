from detroit.types import Scaler
from .types import ColorScheme
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions
from .properties import Margin

__all__ = ["Context"]

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
    def x(self) -> Scaler:
        return self._x

    @property
    def y(self) -> Scaler:
        return self._y

    @property
    def x_label(self) -> str | None:
        return self._x_label

    @property
    def y_label(self) -> str | None:
        return self._y_label

    @property
    def width(self) -> str:
        return self._width

    @property
    def height(self) -> str:
        return self._height

    @property
    def margin(self) -> Margin:
        return self._margin

    @property
    def color(self) -> str:
        return self._style_options.color

    @property
    def font_size(self) -> int:
        return self._style_options.font_size

    @property
    def font_family(self) -> str:
        return self._style_options.font_family

    @property
    def background(self) -> str:
        return self._style_options.background

    @property
    def color_scheme(self) -> ColorScheme:
        return self._color_options.scheme
