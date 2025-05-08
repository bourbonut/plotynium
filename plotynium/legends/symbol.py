from itertools import accumulate
from functools import reduce
from operator import iadd
import detroit as d3
from detroit.selection import Selection
from ..schemes import Scheme
from .string_widths import STRING_WIDTHS
from ..interpolations import Interpolation


def symbol_legend(
    svg: Selection,
    labels: list,
    margin_left: int,
    margin_top: int,
    scheme: Interpolation | Scheme,
    font_size: int = 12,
):
    """
    Adds to the SVG input, a legend described by labels associated with symbols

    Parameters
    ----------
    svg : Selection
        SVG on which the legend will be added
    labels : list
        Labels to make the legend
    margin_left : int
        Margin left value
    margin_top : int
        Margin top value
    scheme : Interpolation | Scheme
        Color scheme
    font_size : int
        Font size of labels
    """
    if not labels:
        return
    symbol_size = 5
    ratio = font_size / 2
    lengths = [reduce(iadd, [STRING_WIDTHS.get(char, 1) for char in str(label)], 0) for label in labels]
    offsets = [0] + [6 * symbol_size + length * ratio for length in lengths[:-1]]
    offsets = list(accumulate(offsets))

    symbol_type = d3.scale_ordinal(labels, d3.SYMBOLS_STROKE)
    color = d3.scale_sequential([0, len(labels) - 1], scheme)

    legend = (
        svg.append("g")
        .attr("class", "legend")
        .attr("transform", f"translate({margin_left // 2}, {margin_top // 2})")
        .select_all("legend")
        .data(labels)
        .enter()
    )

    g = (
        legend.append("g")
        .attr("transform", lambda _, i: f"translate({offsets[i]}, 0)")
    )

    (
        g.append("path")
        .attr("d", lambda d: d3.symbol(symbol_type(d))())
        .style("stroke", lambda _, i: color(i))
        .style("fill", "none")
    )

    (
        g.append("text")
        .attr("x", symbol_size * 1.5 + 4)
        .attr("y", font_size // 3)
        .text(lambda d: str(d))
        .style("fill", "currentColor")
        .style("font-size", font_size)
    )
