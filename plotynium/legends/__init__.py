import detroit as d3
from detroit.selection import Selection

from ..context import Context
from ..marks import Mark
from ..properties import LegendProperties
from ..transformers import Constant
from ..types import ColorScheme
from .continuous_color import ContinuousLegend
from .default_scheme import default_colorscheme
from .discrete_color import DiscreteLegend
from .symbol import SymbolLegend

__all__ = ["Legend"]


class Legend(DiscreteLegend, ContinuousLegend, SymbolLegend, Mark):
    """
    Special mark which has its own definition for making a legend. Legend is
    located on top of the main canvas where all other marks are applied. Given
    the value of `color_mapping` and `symbol_mapping` arguments, this class
    takes decision to know if the legend should be _continuous_, _discrete with
    squares_ or _discrete with symbols_.

    Parameters
    ----------
    color_mapping : list[tuple[str, str]] | None
        List of pairs (label, color)
    symbol_mapping : list[tuple[str, str]] | None
        List of pairs (label, symbol path)
    scheme : ColorScheme | None
        Color scheme
    square_size : int
        Square_size (only for discrete legend)
    symbol_size : int
        Symbol size (only for symbol legend)
    fill : str | None
        Fill color for text
    fill_opacity : float
        Fill opacity
    stroke : str | None
        Stroke color for text
    stroke_opacity : float
        Stroke opacity
    stroke_width : float
        Stroke width (only for continuous legend)
    font_size : int
        Font size for text
    width : int
        Width size
    height : int
        Height size
    margin_top : int
        Margin top value
    margin_left : int
        Margin left value
    margin_bottom : int
        Margin bottom value
    margin_right : int
        Margin right value
    """

    def __init__(
        self,
        color_mapping: list[tuple[str, str]] | None = None,
        symbol_mapping: list[tuple[str, str]] | None = None,
        scheme: ColorScheme | None = None,
        square_size: int = 15,
        symbol_size: int = 5,
        fill: str | None = None,
        fill_opacity: float = 1.0,
        stroke: str | None = None,
        stroke_opacity: float = 1.0,
        stroke_width: float = 1.0,
        font_size: int = 12,
        width: int = 240,
        height: int = 50,
        margin_top: int = 21,
        margin_left: int = 15,
        margin_bottom: int = 21,
        margin_right: int = 15,
    ):
        Mark.__init__(self)
        self._color_mapping = color_mapping or [
            (str(x), "none") for x in d3.ticks(0, 1, 10)
        ]
        self._symbol_mapping = symbol_mapping or []
        self._scheme = scheme
        self._square_size = square_size
        self._symbol_size = symbol_size
        self._fill = Constant(fill or "currentColor")
        self._fill_opacity = fill_opacity
        self._stroke = Constant(stroke or "currentColor")
        self._stroke_opacity = stroke_opacity
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
    def properties(self) -> LegendProperties:
        """
        Returns its properties

        Returns
        -------
        LegendProperties
            Own properties
        """
        return self._properties

    def apply(self, svg: Selection, ctx: Context):
        """
        Adds a legend on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx : Context
            Context
        """
        # Updates attributes from context
        self._properties = ctx.legend_properties
        self._font_size = ctx.font_size
        self._scheme = (
            self._scheme
            or ctx.color_scheme
            or default_colorscheme(len(self._color_mapping))
        )

        # Adds the legend on the SVG given arguments
        if len(self._symbol_mapping) > 0:
            self.symbol_legend(svg)
        elif len(self._color_mapping) > 10:
            self.continuous_color_legend(svg)
        else:
            self.discrete_color_legend(svg)
