import detroit as d3
from detroit.selection import Selection

from .context import Context
from .dimensions import dimensions
from .legends import Legend
from .marks import AxisX, AxisY, GridX, GridY, Mark, check_types
from .options import (
    ColorOptions,
    StyleOptions,
    SymbolOptions,
    XOptions,
    YOptions,
    init_options,
)
from .properties import Margin
from .scaler import determine_label, make_scaler


def plot(
    marks: list[Mark],
    width: int | None = None,
    height: int | None = None,
    margin_top: int = 10,
    margin_left: int = 45,
    margin_bottom: int = 45,
    margin_right: int = 10,
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
    x_options = init_options(x, XOptions)
    y_options = init_options(y, YOptions)
    color_options = init_options(color, ColorOptions)
    style_options = init_options(style, StyleOptions)
    symbol_options = init_options(symbol, SymbolOptions)

    user_legend_option = color_options.legend or symbol_options.legend
    margin = Margin(margin_top, margin_left, margin_bottom, margin_right)
    width, height, canvas_properties, legend_properties = dimensions(
        marks,
        user_legend_option,
        width,
        height,
        margin,
    )

    # Set labels
    x_label = x_options.label
    y_label = y_options.label
    if x_label is None and y_label is None:
        x_label = determine_label([mark.x_label for mark in marks])
        y_label = determine_label([mark.y_label for mark in marks])

    # Set scalers
    x_scaler_types = [mark.x_scaler_type for mark in marks]
    y_scaler_types = [mark.y_scaler_type for mark in marks]

    x_domains = [mark.x_domain for mark in marks]
    y_domains = [mark.y_domain for mark in marks]

    x_ranges = [margin.left, canvas_properties.width - margin.right]
    y_ranges = [canvas_properties.height - margin.bottom, margin.top]

    x = x_scale = make_scaler(x_scaler_types, x_domains, x_ranges, nice=x_options.nice)
    y = y_scale = make_scaler(y_scaler_types, y_domains, y_ranges, nice=y_options.nice)

    # Creates a context shared between marks and legend
    ctx = Context(
        canvas_properties,
        legend_properties,
        x_options,
        y_options,
        color_options,
        style_options,
        symbol_options,
        x_scale,
        y_scale,
        x_label,
        y_label,
    )

    # Conditions to check if the mark is unique
    only_legend = len(marks) == 1 and check_types(Legend)(marks[0])
    only_axis_x = len(marks) == 1 and check_types(AxisX)(marks[0])
    only_axis_y = len(marks) == 1 and check_types(AxisY)(marks[0])
    is_not_unique = not (only_legend or only_axis_x or only_axis_y)

    # Checks if legend is True or if it exists
    legend_marks = list(filter(check_types(Legend), marks))
    add_legend = len(legend_marks) > 0 or user_legend_option

    if is_not_unique:
        # Set x axis
        if not any(map(check_types(AxisX), marks)):
            x_ticks = x.ticks() if hasattr(x, "ticks") else x.get_domain()
            x_tick_format = (
                x.tick_format(x_options.count, x_options.specifier)
                if hasattr(x, "tick_format")
                else x.get_domain()
            )
            marks.append(
                AxisX(
                    x_ticks,
                    tick_format=x_tick_format,
                    label=x_label,
                    fill=style_options.color,
                )
            )

        # Set y axis
        if not any(map(check_types(AxisY), marks)):
            y_ticks = y.ticks() if hasattr(y, "ticks") else y.get_domain()
            y_tick_format = (
                y.tick_format(y_options.count, y_options.specifier)
                if hasattr(y, "tick_format")
                else y.get_domain()
            )
            marks.append(
                AxisY(
                    y_ticks,
                    tick_format=y_tick_format,
                    label=y_label,
                    fill=style_options.color,
                )
            )

        # Set x grid
        if not any(map(check_types(GridX), marks)) and x_options.grid or grid:
            x_ticks = x.ticks() if hasattr(x, "ticks") else x.get_domain()
            marks.append(GridX(x_ticks))

        # Set y grid
        if not any(map(check_types(GridY), marks)) and y_options.grid or grid:
            y_ticks = y.ticks() if hasattr(y, "ticks") else y.get_domain()
            marks.append(GridY(y_ticks))

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
        .style("font-size", f"{ctx.font_size}px")
        .style("font-family", ctx.font_family)
    )

    default_style = StyleOptions()
    if ctx.background != default_style.background:
        svg.style("background", ctx.background)
    if ctx.color != default_style.color:
        svg.style("color", ctx.color)

    if add_legend:
        legend_group = svg.append("g").attr("class", "legend")

    if not only_legend:
        canvas_group = svg.append("g").attr("class", "canvas")
        if translate := ctx.canvas_translate:
            canvas_group.attr("transform", translate)

        # Apply mark on SVG content
        for mark in marks:
            mark.apply(canvas_group, ctx)

    if add_legend:
        # Gets legend or creates new one
        legend = Legend(
            ctx.color_mapping,
            ctx.symbol_mapping,
            ctx.color_scheme,
        )
        if len(legend_marks) > 0:
            legend = legend_marks[0]
        legend.apply(legend_group, ctx)

    return svg
