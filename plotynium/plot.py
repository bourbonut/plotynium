from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions, init_options
from .symbols import symbol_legend
from .scaler import Scaler, make_scaler
from . import label, domain

import detroit as d3


def plot(
    marks: list,
    width: int = 640,
    height: int = 438,
    margin_top: int = 10,
    margin_right: int = 10,
    margin_bottom: int = 45,
    margin_left: int = 45,
    grid: bool = False,
    x: XOptions | dict | None = None,
    y: YOptions | dict | None = None,
    color: ColorOptions | dict | None = None,
    style: StyleOptions | dict | None = None,
    symbol: SymbolOptions | dict | None = None,
):
    width = width or 640
    height = height or 438
    x_options = init_options(x, XOptions)
    y_options = init_options(y, YOptions)
    color_options = init_options(color, ColorOptions)
    style_options = init_options(style, StyleOptions)
    symbol_options = init_options(symbol, SymbolOptions)
    margin_top = max(margin_top, 40) if symbol_options.legend else margin_top

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
        .style("font-size", f"{style_options.font_size}px")
        .style("font-family", style_options.font_family)
    )

    default_style = StyleOptions()
    if style_options.background != default_style.background:
        svg.style("background", style_options.background)
    if style_options.color != default_style.color:
        svg.style("color", style_options.color)

    # Set labels
    x_label = x_options.label
    y_label = y_options.label
    if x_label is None and y_label is None:
        x_label = label.reduce([mark.x_label for mark in marks])
        y_label = label.reduce([mark.y_label for mark in marks])

    x_scaler_types = [mark.x_scaler_type for mark in marks]
    y_scaler_types = [mark.y_scaler_type for mark in marks]

    x_domains = [mark.x_domain for mark in marks]
    y_domains = [mark.y_domain for mark in marks]

    x_ranges = [margin_left, width - margin_right]
    y_ranges = [height - margin_bottom, margin_top]

    x = make_scaler(x_scaler_types, x_domains, x_ranges, nice=x_options.nice)
    y = make_scaler(y_scaler_types, y_domains, y_ranges, nice=y_options.nice)

    for mark in marks:
        mark.scheme = color_options.scheme
        mark(svg, x, y, height=height, margin_left=margin_left, margin_bottom=margin_bottom)

    if symbol_options.legend:
        for mark in marks:
            if hasattr(mark, "_labels"):
                symbol_legend(svg, mark._labels, margin_left, margin_top, color_options.scheme, style_options.font_size)
                break
    
    return svg
