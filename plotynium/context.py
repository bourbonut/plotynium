from detroit.types import Scaler
from .types import ColorScheme
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions
from .properties import Margin, CanvasProperties, LegendProperties

__all__ = ["Context"]

class Context:
    def __init__(
        self,
        canvas_properties: CanvasProperties,
        legend_properties: LegendProperties,
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
        self._canvas_properties = canvas_properties
        self._legend_properties = legend_properties

        self._x_options = x_options
        self._y_options = y_options
        self._color_options = color_options
        self._style_options = style_options
        self._symbol_options = symbol_options

        self._color_mapping = []
        self._symbol_mapping = []

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
        return self._canvas_properties.width

    @property
    def height(self) -> str:
        return self._canvas_properties.height

    @property
    def margin(self) -> Margin:
        return self._canvas_properties.margin

    @property
    def canvas_translate(self) -> str | None:
        return self._canvas_properties.translate

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

    @property
    def labels(self) -> dict[int, str]:
        return self._color_options.labels

    @property
    def legend_properties(self) -> LegendProperties:
        return self._legend_properties

    @property
    def color_mapping(self) -> list[tuple[str, str]]:
        return self._color_mapping

    @property
    def symbol_mapping(self) -> list[tuple[str, str]]:
        return self._symbol_mapping

    def update_color_mapping(self, *color_mappings: tuple[list[tuple[str, str]]]):
        color_mappings = [self._color_mapping] + list(color_mappings)
        self._color_mapping = max(color_mappings, key=len)

    def update_symbol_mapping(self, *symbol_mappings: tuple[list[tuple[str, str]]]):
        symbol_mappings = [self._symbol_mapping] + list(symbol_mappings)
        self._symbol_mapping = max(symbol_mappings, key=len)
