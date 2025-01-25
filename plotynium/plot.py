from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable

import detroit as d3

Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

def reduce_domain(domains):
    mins = list(map(itemgetter(0), domains))
    maxs = list(map(itemgetter(1), domains))
    return [min(mins), max(maxs)]

def reduce_label(labels):
    labels = set(labels)
    if len(labels) == 1:
        if label := labels.pop():
            return label

def plot(
    marks: list,
    width: int | None = None,
    height: int | None = None,
    margin: tuple[int, int, int, int] | None = None,
    color_scheme: Callable | None = None,
    style: dict | None = None,
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

    x_domain = reduce_domain([mark.x_domain for mark in marks])
    y_domain = reduce_domain([mark.y_domain for mark in marks])

    x_label = reduce_label([mark.x_label for mark in marks])
    y_label = reduce_label([mark.y_label for mark in marks])

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
        mark.set_color_scheme(color_scheme)
        mark(svg, width, height, margin, x, y)

    return svg
