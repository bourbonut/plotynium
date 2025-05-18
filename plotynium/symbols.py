from enum import Enum

import detroit as d3


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
