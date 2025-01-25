from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable
from .options import StyleOptions, ColorOptions, SymbolOptions
from . import label, domain

import detroit as d3

Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

def plot(
    marks: list,
    width: int | None = None,
    height: int | None = None,
    margin: tuple[int, int, int, int] | None = None,
    color: ColorOptions | None = None,
    style: StyleOptions | None = None,
    symbol: SymbolOptions | None = None,
):
    width = width or 640
    height = height or 438
    margin = Margin(*(margin or [20, 30, 30, 40]))
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

    x_domain = domain.reduce([mark.x_domain for mark in marks])
    y_domain = domain.reduce([mark.y_domain for mark in marks])

    x_label = label.reduce([mark.x_label for mark in marks])
    y_label = label.reduce([mark.y_label for mark in marks])

    x = (
        d3.scale_linear()
        .set_domain(x_domain)
        .nice()
        .set_range([margin.left, width - margin.right])
    )

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
        mark(svg, width, height, margin, x, y)

    return svg
