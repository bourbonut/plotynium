import detroit as d3
from detroit.selection.selection import Selection
from enum import Enum
from .schemes import Scheme
from .interpolations import Interpolation

class SymbolFill(Enum):
    """
    All available symbols with `fill` attribute for changing its color
    """
    CIRCLE = d3.symbol_circle
    CROSS = d3.symbol_cross
    DIAMOND = d3.symbol_diamond
    SQUARE = d3.symbol_square
    STAR = d3.symbol_star
    TRIANGLE = d3.symbol_triangle
    WYE = d3.symbol_wye

class SymbolStroke(Enum):
    """
    All available symbols with `stroke` attribute for changing its color
    """
    ASTERISK = d3.symbol_asterisk
    CIRCLE = d3.symbol_circle
    DIAMOND = d3.symbol_diamond2
    PLUS = d3.symbol_plus
    SQUARE = d3.symbol_square2
    TIMES = d3.symbol_times
    TRIANGLE = d3.symbol_triangle2

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
    nb_columns = len(labels)
    symbol_size = 5
    label_length = max(map(lambda label: len(str(label)), labels)) * 3
    offset = 2 * (symbol_size + label_length) + 16

    symbol_type = d3.scale_ordinal(labels, d3.SYMBOLS_STROKE)
    color = d3.scale_sequential([0, len(labels)], scheme)

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
        .attr("transform", lambda _, i: f"translate({i * offset}, 0)")
    )

    (
        g.append("path")
        .attr("d", lambda d: d3.symbol(symbol_type(d))())
        .style("stroke", lambda _, i: color(i))
        .style("fill", "none")
    )

    (
        g.append("text")
        .attr("x", symbol_size * 0.5 + label_length + 4)
        .attr("y", font_size // 3)
        .text(lambda d: str(d))
        .style("fill", "currentColor")
        .style("font-size", font_size)
    )
