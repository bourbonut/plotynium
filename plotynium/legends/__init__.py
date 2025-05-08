import detroit as d3
from detroit.selection import Selection
from ..interpolations import Interpolation
from ..schemes import Scheme
from itertools import accumulate
from functools import reduce
from operator import iadd
from .string_widths import STRING_WIDTHS
from ..context import Context, MarkContext

__all__ = ["Legend"]

class Legend:

    def __init__(
        self,
        labels_mapping: list[tuple[str, str]] | None = None,
        symbols_mapping: list[tuple[str, str]] | None = None,
        scheme: Interpolation | Scheme | None = None,
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
        self._labels_mapping = labels_mapping or d3.ticks(0, 1, 10)
        self._symbols_mapping = symbols_mapping or []
        self._scheme = scheme or Interpolation.RAINBOW
        self._square_size = square_size
        self._symbol_size = self._symbol_size
        self._rows = rows
        self._fill = fill
        self._fill_opacity = fill_opacity
        self._stroke = stroke
        self._stroke_opactity = stroke_opacity
        self._stroke_width = stroke_width
        self._font_size = font_size

        self.context: MarkContext | None = None

    def set_context(self, context: Context):
        self._font_size = context.get_font_size()
        self._scheme = context.get_color_scheme()
        self.context = context.get_mark_context(0)
        self.context.horizontal_split(40)

    def apply(self, context: Context):
        pass

    def discrete_color_legend(svg: Selection):
        """
        Adds to the SVG input, a legend described by labels associated with rectangles

        Parameters
        ----------
        svg : Selection
            SVG on which the legend will be added
        """
        pass
        # rect_size = 15
        # ratio = font_size / 2
        # lengths = [reduce(iadd, [STRING_WIDTHS.get(char, 1) for char in str(label)], 0) for label in labels]
        # offsets = [0] + [2 * rect_size + length * ratio for length in lengths[:-1]]
        # offsets = list(accumulate(offsets))
        #
        # color = d3.scale_sequential([0, len(labels) - 1], scheme)
        #
        # legend = (
        #     svg.append("g")
        #     .attr("class", "legend")
        #     .attr("transform", f"translate({margin_left // 2}, {margin_top // 2})")
        #     .select_all("legend")
        #     .data(labels)
        #     .enter()
        # )
        #
        # g = (
        #     legend.append("g")
        #     .attr("transform", lambda _, i: f"translate({offsets[i]}, 0)")
        # )
        #
        # (
        #     g.append("rect")
        #     .attr("x", -rect_size / 2)
        #     .attr("y", -rect_size / 2)
        #     .attr("width", rect_size)
        #     .attr("height", rect_size)
        #     .attr("fill", lambda _, i: color(i))
        #     .style("stroke", "none")
        # )
        #
        # (
        #     g.append("text")
        #     .attr("x", rect_size * 0.5 + 4)
        #     .attr("y", font_size // 3)
        #     .text(lambda d: str(d))
        #     .style("fill", "currentColor")
        #     .style("font-size", font_size)
        # )
    
    def symbol_legend(self, svg: Selection):
        """
        Adds to the SVG input, a legend described by labels associated with symbols

        Parameters
        ----------
        svg : Selection
            SVG on which the legend will be added
        """
        if not self._labels_mapping:
            return
        # ratio = self._font_size / 2
        # lengths = [reduce(iadd, [STRING_WIDTHS.get(char, 1) for char in str(label)], 0) for label in labels]
        # offsets = [0] + [6 * self._symbol_size + length * ratio for length in lengths[:-1]]
        # offsets = list(accumulate(offsets))
        #
        # symbol_type = d3.scale_ordinal(labels, d3.SYMBOLS_STROKE)
        # color = d3.scale_sequential([0, len(labels) - 1], scheme)
        #
        # legend = (
        #     svg.append("g")
        #     .attr("class", "legend")
        #     .attr("transform", f"translate({margin_left // 2}, {margin_top // 2})")
        #     .select_all("legend")
        #     .data(labels)
        #     .enter()
        # )
        #
        # g = (
        #     legend.append("g")
        #     .attr("transform", lambda _, i: f"translate({offsets[i]}, 0)")
        # )
        #
        # (
        #     g.append("path")
        #     .attr("d", lambda d: d3.symbol(symbol_type(d))())
        #     .style("stroke", lambda _, i: color(i))
        #     .style("fill", "none")
        # )
        #
        # (
        #     g.append("text")
        #     .attr("x", self._symbol_size * 1.5 + 4)
        #     .attr("y", font_size // 3)
        #     .text(lambda d: str(d))
        #     .style("fill", "currentColor")
        #     .style("font-size", font_size)
        # )
