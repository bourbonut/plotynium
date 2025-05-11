from .marks import AxisX, AxisY, GridX, GridY, Mark
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions, init_options
from .scaler import make_scaler
from .context import Context
from .legends import Legend
from . import label
from math import sqrt
from functools import partial

import detroit as d3
from detroit.selection import Selection

def auto_width(legend_width: bool, only_legend: bool, has_legend: bool):
    if only_legend and has_legend:
        return legend_width
    else:
        return 640

def auto_height(
    width: int,
    legend_height: int,
    only_axis: bool,
    axis_is_x: bool,
    has_legend: bool,
    only_legend: bool,
):
    if (only_legend and has_legend) or (only_axis and axis_is_x):
        return legend_height
    elif has_legend:
        return legend_height + int(width / sqrt(2))
    return int(width / sqrt(2))

def plot(
    marks: list[Mark],
    margin_top: int = 10,
    margin_left: int = 45,
    margin_bottom: int = 45,
    margin_right: int = 10,
    width: int | None = None,
    height: int | None = None,
    grid: bool = False,
    x: XOptions | dict | None = None,
    y: YOptions | dict | None = None,
    color: ColorOptions | dict | None = None,
    style: StyleOptions | dict | None = None,
    symbol: SymbolOptions | dict | None = None,
) -> Selection:
    """
    Generates a SVG plot from the given marks and different specified options

    Parameters
    ----------
    marks : list[Mark]
        List of marks represented on the plot
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
    grid : bool
        `True` to add all lines to form a grid
    x : XOptions | dict | None
        X axis options
    y : YOptions | dict | None
        Y axis options
    color : ColorOptions | dict | None
        Color scheme options
    style : StyleOptions | dict | None
        Style options
    symbol : SymbolOptions | dict | None
        Symbol options

    Returns
    -------
    Selection
        Generated SVG plot
    """
    # Prepare options
    marks = list(marks)
    if len(marks) == 0:
        raise ValueError("Empty list of marks")
    x_options = init_options(x, XOptions)
    y_options = init_options(y, YOptions)
    color_options = init_options(color, ColorOptions)
    style_options = init_options(style, StyleOptions)
    symbol_options = init_options(symbol, SymbolOptions)

    # Mark types
    def check_types(*types):
        return lambda mark: isinstance(mark, tuple(types))

    axis_marks = list(filter(check_types(AxisX, AxisY), marks))
    only_axis = len(axis_marks) == 1
    axis_is_x = isinstance(axis_marks[0], AxisX) if only_axis else False
    legend_marks = list(filter(check_types(Legend), marks))
    has_legend = len(legend_marks) >= 1 or color_options.legend or symbol_options.legend
    only_legend = len(legend_marks) == 1
    legend_width = 240
    legend_height = 50
    if len(legend_marks) > 1:
        raise ValueError("There can be only one legend.")
    elif len(legend_marks) == 1:
        legend_width = legend_marks[0]._width
        legend_height = legend_marks[0]._height

    # Set dimensions
    width = width or auto_width(legend_width, only_legend, has_legend)
    height = height or auto_height(
        width, legend_height, only_axis, axis_is_x, has_legend, only_legend
    )

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

    # # Set x axis
    # if not any(map(lambda mark: isinstance(mark, AxisX), marks)):
    #     x_ticks = x.ticks() if hasattr(x, "ticks") else x.domain
    #     x_tick_format = x.tick_format() if hasattr(x, "tick_format") else x.domain
    #     marks.append(AxisX(x_ticks, tick_format=x_tick_format, label=x_label, fill=style_options.color))
    #
    # # Set y axis
    # if not any(map(lambda mark: isinstance(mark, AxisY), marks)):
    #     y_ticks = y.ticks() if hasattr(y, "ticks") else y.domain
    #     y_tick_format = y.tick_format() if hasattr(y, "tick_format") else y.domain
    #     marks.append(AxisY(y_ticks, tick_format=y_tick_format, label=y_label, fill=style_options.color))
    #
    # # Set x grid
    # if not any(map(lambda mark: isinstance(mark, GridX), marks)) and x_options.grid or grid:
    #     x_ticks = x.ticks() if hasattr(x, "ticks") else x.domain
    #     marks.append(GridX(x_ticks))
    #
    # # Set y grid
    # if not any(map(lambda mark: isinstance(mark, GridY), marks)) and y_options.grid or grid:
    #     y_ticks = y.ticks() if hasattr(y, "ticks") else y.domain
    #     marks.append(GridY(y_ticks))

    # Set legend
    # legend = None
    # found = False
    # for mark in marks:
    #     if isinstance(mark, Legend):
    #         legend = mark
    #         found = True
    #         continue
    # if not found and (color_options.legend or symbol_options.legend):
    #     legend = Legend()

    context = Context(
        x,
        y,
        width,
        height,
        margin_top,
        margin_left,
        margin_bottom,
        margin_right,
        style_options.font_size,
        color_options.scheme,
    )

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

    # Apply mark on SVG content
    for mark in marks:
        mark.apply(svg, context)

    # if legend is not None:
    #     legend.apply(svg, context)

    return svg
