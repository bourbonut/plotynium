from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions
from .symbols import symbol_legend
from .scaler import Scaler, make_scaler
from . import label, domain

import detroit as d3


def plot(
    marks: list,
    width: int = 640,
    height: int = 438,
    margin_top: int = 20,
    margin_right: int = 10,
    margin_bottom: int = 40,
    margin_left: int = 40,
    x: XOptions | None = None,
    y: YOptions | None = None,
    color: ColorOptions | None = None,
    style: StyleOptions | None = None,
    symbol: SymbolOptions | None = None,
):
    width = width or 640
    height = height or 438
    x_options = x or XOptions()
    y_options = y or YOptions()
    color_options = color or ColorOptions()
    style_options = style or StyleOptions()
    symbol_options = symbol or SymbolOptions()
    if symbol_options.legend:
        margin_top += 20

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

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
   
    x_axis = (
        svg.append("g")
        .attr("transform", f"translate(0, {height - margin_bottom})")
        .call(d3.axis_bottom(x))
        .call(lambda g: g.select(".domain").remove())
    )
    if x_options.grid:
        x_axis.call(lambda g: g.select_all(".tick")
            .select_all("line")
            .clone()
            .attr("y2", -height + margin_top + margin_bottom)
            .attr("stroke-opacity", 0.1)
        )
    if x_label is not None:
        x_axis.call(
            lambda g: g.append("text")
            .attr("x", (x_ranges[0] + x_ranges[1]) // 2 + 3 * len(x_label))
            .attr("y", (margin_top + margin_bottom) // 2 - 10)
            .attr("fill", "#000")
            .attr("font-weight", "bold")
            .attr("text-anchor", "end")
            .text(x_label)
        )

    y_axis = (
        svg.append("g")
        .attr("transform", f"translate({margin_left}, 0)")
        .call(d3.axis_left(y))
        .call(lambda g: g.select(".domain").remove())
    )
    if y_options.grid:
        y_axis.call(lambda g: g.select_all(".tick")
            .select_all("line")
            .clone()
            .attr("x2", width - margin_left - margin_right)
            .attr("stroke-opacity", 0.1)
        )
    if y_label is not None:
        y_axis.call(
            lambda g: g.select(".tick:last-of-type")
            .select("text")
            .clone()
            .attr("x", 4)
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text(y_label)
        )

    for mark in marks:
        mark.set_color_scheme(color_options.scheme)
        mark(svg, x, y)
 
    if symbol_options.legend:
        for mark in marks:
            if hasattr(mark, "_labels"):
                symbol_legend(svg, mark._labels, margin_left, margin_top, color_options.scheme)
                break
    
    return svg
