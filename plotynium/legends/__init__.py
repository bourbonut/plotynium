import detroit as d3
from detroit.selection import Selection
from ..types import ColorScheme
from ..context import Context
from ..transformers import Constant
from .discrete_color import DiscreteLegend
from .continuous_color import ContinuousLegend
from .symbol import SymbolLegend
from .default_scheme import default_colorscheme
from ..marks import Mark

__all__ = ["Legend"]

class Legend(DiscreteLegend, ContinuousLegend, SymbolLegend, Mark):

    def __init__(
        self,
        labels_mapping: list[tuple[str, str]] | None = None,
        symbols_mapping: list[tuple[str, str]] | None = None,
        width: int | None = None,
        height: int | None = None,
        scheme: ColorScheme | None = None,
        square_size: int = 15,
        symbol_size: int = 5,
        rows: int = 1,
        fill: str | None = None,
        fill_opacity: float = 1.,
        stroke: str | None = None,
        stroke_opacity: float = 1.,
        stroke_width: float = 1.,
        font_size: int = 12,
    ):
        Mark.__init__(self)
        self._width = width or 240
        self._height = height or 50
        self._labels_mapping = labels_mapping or [(str(x), "none") for x in d3.ticks(0, 1, 10)]
        self._symbols_mapping = symbols_mapping or []
        self._scheme = scheme
        self._square_size = square_size
        self._symbol_size = symbol_size
        self._rows = rows
        self._fill = Constant(fill or "black")
        self._fill_opacity = fill_opacity
        self._stroke = Constant(stroke or "black")
        self._stroke_opactity = stroke_opacity
        self._stroke_width = stroke_width
        self._font_size = font_size

    def update(self, context: Context):
        self._font_size = context.font_size
        self._scheme = (
            self._scheme or
            context.color_scheme or
            default_colorscheme(len(self._labels_mapping))
        )

    def apply(self, svg: Selection, context: Context):
        self.update(context)
        if len(self._symbols_mapping) > 0:
            self.symbol_legend(svg)
        elif len(self._labels_mapping) > 10:
            self.continuous_color_legend(svg)
        else:
            self.discrete_color_legend(svg)
