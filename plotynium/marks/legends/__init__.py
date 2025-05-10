import detroit as d3
from detroit.selection import Selection
from ...types import ColorScheme
from ...context import Context
from .discrete_color import DiscreteLegend
from .continuous_color import ContinuousLegend
from .symbol import SymbolLegend
from .default_scheme import default_colorscheme
from ..mark import Mark

__all__ = ["Legend"]

class Legend(DiscreteLegend, ContinuousLegend, SymbolLegend, Mark):

    def __init__(
        self,
        labels_mapping: list[tuple[str, str]] | None = None,
        symbols_mapping: list[tuple[str, str]] | None = None,
        scheme: ColorScheme | None = None,
        square_size: int = 15,
        symbol_size: int = 5,
        rows: int = 1,
        fill: str | None = None,
        fill_opacity: float = 1.,
        stroke: str | None = None,
        stroke_opacity: float = 1.,
        stroke_width: float = 1.5,
        font_size: int = 12,
    ):
        self._labels = labels_mapping or d3.ticks(0, 1, 10)
        self._symbols = symbols_mapping or []
        self._scheme = scheme or default_colorscheme(len(self._labels))
        self._square_size = square_size
        self._symbol_size = symbol_size
        self._rows = rows
        self._fill = fill
        self._fill_opacity = fill_opacity
        self._stroke = stroke
        self._stroke_opactity = stroke_opacity
        self._stroke_width = stroke_width
        self._font_size = font_size

    def apply(self, svg: Selection, context: Context):
        self._font_size = context.get_font_size()
        self._scheme = context.get_color_scheme()
        self.discrete_color_legend(svg)
