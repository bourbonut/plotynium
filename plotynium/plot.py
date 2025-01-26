from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions
from .scaler import Scaler, characterize_scaler
from . import label, domain

import detroit as d3

Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

def plot(
    marks: list,
    width: int | None = None,
    height: int | None = None,
    margin: tuple[int, int, int, int] | None = None,
    x: XOptions | None = None,
    y: YOptions | None = None,
    color: ColorOptions | None = None,
    style: StyleOptions | None = None,
    symbol: SymbolOptions | None = None,
):
    width = width or 640
    height = height or 438
    margin = Margin(*(margin or [20, 30, 30, 40]))
    x_options = x or XOptions()
    y_options = y or YOptions()

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

    # Set domains
    x_domain = domain.reduce([mark.x_domain for mark in marks])
    y_domain = domain.reduce([mark.y_domain for mark in marks])

    # Set labels
    x_label = x_options.label
    y_label = y_options.label
    if x_label is None and y_label is None:
        x_label = label.reduce([mark.x_label for mark in marks])
        y_label = label.reduce([mark.y_label for mark in marks])

    expected_scaler = characterize_scaler([mark._expected_scaler for mark in marks])

    if expected_scaler == Scaler.CONTINOUS:
        x = (
            d3.scale_linear()
            .set_domain(x_domain)
            .nice()
            .set_range([margin.left, width - margin.right])
        )
    elif expected_scaler == Scaler.TIME:
        x = (
            d3.scale_time()
            .set_domain(x_domain)
            .set_range([margin.left, width - margin.right])
        )
    elif expected_scaler == Scaler.BAND:
        x = (
            d3.scale_band()
            .set_domain(x_domain)
            .set_range([margin.left, width - margin.right])
            .set_padding(0.1)
        )
    else:
        raise ValueError(f"Undefined scaler (found {expected_scaler})")

    y = (
        d3.scale_linear()
        .set_domain(y_domain)
        .nice()
        .set_range([height - margin.bottom, margin.top])
    )
    
    x_axis = (
        svg.append("g")
        .attr("transform", f"translate(0, {height - margin.bottom})")
        .call(d3.axis_bottom(x))
        .call(lambda g: g.select(".domain").remove())
    )
    if x_options.grid:
        x_axis.call(lambda g: g.select_all(".tick")
            .select_all("line")
            .clone()
            .attr("y2", -height + margin.top + margin.bottom)
            .attr("stroke-opacity", 0.1)
        )
    if x_label is not None:
        x_axis.call(
            lambda g: g.append("text")
            .attr("x", width - margin.right)
            .attr("y", -4)
            .attr("fill", "#000")
            .attr("font-weight", "bold")
            .attr("text-anchor", "end")
            .text(x_label)
        )

    y_axis = (
        svg.append("g")
        .attr("transform", f"translate({margin.left}, 0)")
        .call(d3.axis_left(y))
        .call(lambda g: g.select(".domain").remove())
    )
    if y_options.grid:
        y_axis.call(lambda g: g.select_all(".tick")
            .select_all("line")
            .clone()
            .attr("x2", width - margin.left - margin.right)
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
        if color is not None:
            mark.set_color_scheme(color.scheme)
        mark(svg, x, y)

    return svg
