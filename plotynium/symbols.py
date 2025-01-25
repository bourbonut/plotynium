import detroit as d3
from enum import Enum

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
