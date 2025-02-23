from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable
from .marks import AxisX, AxisY, GridX, GridY
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions, init_options
from .symbols import symbol_legend
from .scaler import Scaler, make_scaler
from . import label, domain

import detroit as d3
from detroit.selection.selection import Selection


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
) -> Selection:
    marks = list(marks)
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

    # Set scalers
    x_scaler_types = [mark.x_scaler_type for mark in marks]
    y_scaler_types = [mark.y_scaler_type for mark in marks]

    x_domains = [mark.x_domain for mark in marks]
    y_domains = [mark.y_domain for mark in marks]

    x_ranges = [margin_left, width - margin_right]
    y_ranges = [height - margin_bottom, margin_top]

    x = make_scaler(x_scaler_types, x_domains, x_ranges, nice=x_options.nice)
    y = make_scaler(y_scaler_types, y_domains, y_ranges, nice=y_options.nice)

    # Set x axis
    if not any(map(lambda mark: isinstance(mark, AxisX), marks)):
        x_ticks = x.ticks() if hasattr(x, "ticks") else x.domain
        x_tick_format = x.tick_format() if hasattr(x, "tick_format") else x.domain
        marks.append(AxisX(x_ticks, tick_format=x_tick_format, label=x_label, fill=style_options.color))

    # Set y axis
    if not any(map(lambda mark: isinstance(mark, AxisY), marks)):
        y_ticks = y.ticks() if hasattr(y, "ticks") else y.domain
        y_tick_format = y.tick_format() if hasattr(y, "tick_format") else y.domain
        marks.append(AxisY(y_ticks, tick_format=y_tick_format, label=y_label, fill=style_options.color))

    # Set x grid
    if not any(map(lambda mark: isinstance(mark, GridX), marks)) and x_options.grid or grid:
        x_ticks = x.ticks() if hasattr(x, "ticks") else x.domain
        marks.append(GridX(x_ticks))

    # Set y grid
    if not any(map(lambda mark: isinstance(mark, GridY), marks)) and y_options.grid or grid:
        y_ticks = y.ticks() if hasattr(y, "ticks") else y.domain
        marks.append(GridY(y_ticks))

    for mark in marks:
        mark.scheme = color_options.scheme
        mark(
            svg,
            x,
            y,
            width=width,
            height=height,
            margin_top=margin_top,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
        )

    if symbol_options.legend:
        for mark in marks:
            if hasattr(mark, "_labels"):
                symbol_legend(svg, mark._labels, margin_left, margin_top, color_options.scheme, style_options.font_size)
                break
    
    return svg
