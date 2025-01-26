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
):
    nb_columns = len(labels)
    offset = 40
    symbol_size = 3
    dx = margin_left - symbol_size * 4
    dy = margin_top - 20 - symbol_size * 1.5

    symbol_type = d3.scale_ordinal(labels, d3.SYMBOLS_STROKE)
    color = d3.scale_sequential([min(labels), max(labels)], scheme)

    legend = (
        svg.select_all("legend")
        .data(labels)
        .enter()
        .append("g")
    )

    (
        legend.append("g")
        .attr("transform", lambda _, i: f"translate({i * offset + dx}, {dy})")
        .append("path")
        .attr("d", lambda d: d3.symbol(symbol_type(d))())
        .style("stroke", color)
        .style("fill", "none")
    )

    (
        legend.append("text")
        .attr("x", lambda _, i: i * offset + margin_left)
        .attr("y", margin_top - 20)
        .text(lambda d: str(d))
        .style("fill", "black")
        .style("font-size", 15)
    )
