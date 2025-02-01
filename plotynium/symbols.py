import detroit as d3
from detroit.selection.selection import Selection
from enum import Enum
from .schemes import Scheme

class SymbolFill(Enum):
    CIRCLE = d3.symbol_circle
    CROSS = d3.symbol_cross
    DIAMON = d3.symbol_diamond
    SQUARE = d3.symbol_square
    STAR = d3.symbol_star
    TRIANGLE = d3.symbol_triangle
    WYE = d3.symbol_wye

class SymbolStroke(Enum):
    ASTERISK = d3.symbol_asterisk
    CIRCLE = d3.symbol_circle
    DIAMOND2 = d3.symbol_diamond2
    PLUS = d3.symbol_plus
    SQUARE2 = d3.symbol_square2
    TIMES = d3.symbol_times
    TRIANGLE2 = d3.symbol_triangle2

def symbol_legend(
    svg: Selection,
    labels: list,
    margin_left: int,
    margin_top: int,
    scheme: Scheme,
    font_size: int = 12,
):
    nb_columns = len(labels)
    symbol_size = 5
    label_length = max(map(lambda label: len(str(label)), labels)) * 3
    offset = 2 * (symbol_size + label_length) + 16

    symbol_type = d3.scale_ordinal(labels, d3.SYMBOLS_STROKE)
    color = d3.scale_sequential([min(labels), max(labels)], scheme)

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
        .style("stroke", color)
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
