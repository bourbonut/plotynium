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
from ..properties import LegendProperties, DEFAULT_SQUARE_SIZE, DEFAULT_SYMBOL_SIZE

__all__ = ["Legend"]


class Legend(DiscreteLegend, ContinuousLegend, SymbolLegend, Mark):

    def __init__(
        self,
        color_mapping: list[tuple[str, str]] | None = None,
        symbol_mapping: list[tuple[str, str]] | None = None,
        scheme: ColorScheme | None = None,
        square_size: int = DEFAULT_SQUARE_SIZE,
        symbol_size: int = DEFAULT_SYMBOL_SIZE,
        rows: int = 1,
        fill: str | None = None,
        fill_opacity: float = 1.,
        stroke: str | None = None,
        stroke_opacity: float = 1.,
        stroke_width: float = 1.,
        font_size: int = 12,
        width: int | None = None,
        height: int | None = None,
        margin_top: int = 0,
        margin_left: int = 0,
        margin_bottom: int = 0,
        margin_right: int = 0,
    ):
        Mark.__init__(self)
        self._color_mapping = color_mapping or [(str(x), "none") for x in d3.ticks(0, 1, 10)]
        self._symbol_mapping = symbol_mapping or []
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
        self._properties = LegendProperties.new(
            width,
            height,
            margin_top,
            margin_left,
            margin_bottom,
            margin_right,
        )

    @property
    def properties(self):
        return self._properties

    def apply(self, svg: Selection, ctx: Context):
        # Update attributes from context
        self._properties = ctx.legend_properties
        self._font_size = ctx.font_size
        self._scheme = (
            self._scheme or
            ctx.color_scheme or
            default_colorscheme(len(self._color_mapping))
        )

        if len(self._symbol_mapping) > 0:
            self.symbol_legend(svg)
        elif len(self._color_mapping) > 10:
            self.continuous_color_legend(svg)
        else:
            self.discrete_color_legend(svg)
