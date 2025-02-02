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
        .style("font-size", style_options.font_size)
        .style("font-family", style_options.font_family)
    )

    (
        svg.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "grey")
        .attr("stroke", "none")
    )

    default_style = StyleOptions()
    if style_options.background != default_style.background:
        svg.style("background", style_options.background)
    if style_options.color != default_style.color:
        svg.style("color", style_options.color)

    # Set labels
    x_label = x_options.label
    y_label = y_options.label
    # if x_label is None and y_label is None:
    #     x_label = label.reduce([mark.x_label for mark in marks])
    #     y_label = label.reduce([mark.y_label for mark in marks])

    # x_scaler_types = [mark.x_scaler_type for mark in marks]
    # y_scaler_types = [mark.y_scaler_type for mark in marks]
    #
    # x_domains = [mark.x_domain for mark in marks]
    # y_domains = [mark.y_domain for mark in marks]
    #
    # x_ranges = [margin_left, width - margin_right]
    # y_ranges = [height - margin_bottom, margin_top]
    #
    # x = make_scaler(x_scaler_types, x_domains, x_ranges, nice=x_options.nice)
    # y = make_scaler(y_scaler_types, y_domains, y_ranges, nice=y_options.nice)

    # x_domains = [mark.x_domain for mark in marks]
    # y_domains = [mark.y_domain for mark in marks]

    x_ranges = [margin_left, width - margin_right]
    y_ranges = [height - margin_bottom, margin_top]

    x = make_scaler([Scaler.CONTINOUS], [[0., 1.]], x_ranges, nice=x_options.nice)
    y = make_scaler([Scaler.CONTINOUS], [[0., 1.]], y_ranges, nice=y_options.nice)

    # x_axis = (
    #     svg.append("g")
    #     .attr("transform", f"translate(0, {height - margin_bottom})")
    #     .call(d3.axis_bottom(x))
    #     .call(lambda g: g.attr("font-size", "inherit").attr("font-family", "inherit"))
    #     .call(lambda g: g.select(".domain").remove())
    # )
    #
    # y_axis = (
    #     svg.append("g")
    #     .attr("transform", f"translate({margin_left}, 0)")
    #     .call(d3.axis_left(y))
    #     .call(lambda g: g.attr("font-size", "inherit").attr("font-family", "inherit"))
    #     .call(lambda g: g.select(".domain").remove())
    # )
    #
    # if x_options.grid or grid:
    #     x_axis.call(lambda g: g.select_all(".tick")
    #         .select_all("line")
    #         .clone()
    #         .attr("y2", y.range[1] - y.range[0])
    #         .attr("stroke-opacity", 0.1)
    #     )
    # if x_label is not None:
    #     x_axis.call(
    #         lambda g: g.append("text")
    #         .attr("x", (x.range[0] + x.range[1]) // 2 + 3 * len(x_label))
    #         .attr("y", (margin_bottom + 20) // 2)
    #         .attr("fill", "currentColor")
    #         .attr("font-weight", "bold")
    #         .attr("text-anchor", "end")
    #         .text(x_label)
    #     )
    #
    # if y_options.grid or grid:
    #     y_axis.call(lambda g: g.select_all(".tick")
    #         .select_all("line")
    #         .clone()
    #         .attr("x2", x.range[1] - x.range[0])
    #         .attr("stroke-opacity", 0.1)
    #     )
    # if y_label is not None:
    #     y_axis.call(
    #         lambda g: g.append("text")
    #         .attr("transform", "rotate(-90)")
    #         .attr("x", -(y.range[0] + y.range[1]) // 2 - 3 * len(y_label))
    #         .attr("y", -(margin_left + 20) // 2)
    #         .attr("fill", "currentColor")
    #         .attr("text-anchor", "start")
    #         .attr("font-weight", "bold")
    #         .text(y_label)
    #     )
    #
    for mark in marks:
        mark.scheme = color_options.scheme
        mark(svg, x, y, height=height, margin_left=margin_left, margin_bottom=margin_bottom)
    #
    # if symbol_options.legend:
    #     for mark in marks:
    #         if hasattr(mark, "_labels"):
    #             symbol_legend(svg, mark._labels, margin_left, margin_top, color_options.scheme, style_options.font_size)
    #             break
    
    return svg
