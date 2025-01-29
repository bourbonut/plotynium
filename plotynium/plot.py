from operator import itemgetter
from collections import namedtuple
from collections.abc import Callable
from .options import StyleOptions, ColorOptions, SymbolOptions, XOptions, YOptions
from .symbols import symbol_legend
from .scaler import Scaler, characterize_scaler
from . import label, domain

import detroit as d3

class Margin:

    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

def make_scaler(
    scaler_type: Scaler,
    domains: list,
    range_vals: list,
    nice: bool = False,
):
    if scaler_type == Scaler.CONTINOUS:
        scaler = (
            d3.scale_linear()
            .set_domain(domain.reduce(domains))
            .set_range(range_vals)
        )
    elif scaler_type == Scaler.TIME:
        scaler = (
            d3.scale_time()
            .set_domain(domain.reduce(domains))
            .set_range(range_vals)
        )
    elif scaler_type == Scaler.BAND:
        scaler = (
            d3.scale_band()
            .set_domain(domain.unify(domains))
            .set_range(range_vals)
        )
    else:
        raise ValueError(f"Undefined scaler (found {x_scaler_type})")

    if nice and scaler_type in [Scaler.CONTINOUS, Scaler.TIME]:
        scaler = scaler.nice()

    return scaler


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
    margin = Margin(margin_top, margin_right, margin_bottom, margin_left)
    x_options = x or XOptions()
    y_options = y or YOptions()
    color_options = color or ColorOptions()
    style_options = style or StyleOptions()
    symbol_options = symbol or SymbolOptions()
    if symbol_options.legend:
        margin.top += 20

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

    x_scaler_type = characterize_scaler([mark.x_scaler_type for mark in marks])
    y_scaler_type = characterize_scaler([mark.y_scaler_type for mark in marks])

    x_domains = [mark.x_domain for mark in marks]
    y_domains = [mark.y_domain for mark in marks]

    x_ranges = [margin.left, width - margin.right]
    y_ranges = [height - margin.bottom, margin.top]

    x = make_scaler(x_scaler_type, x_domains, x_ranges, nice=x_options.nice)
    y = make_scaler(y_scaler_type, y_domains, y_ranges, nice=y_options.nice)
   
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
            .attr("x", (x_ranges[0] + x_ranges[1]) // 2 + 3 * len(x_label))
            .attr("y", (margin.top + margin.bottom) // 2 - 10)
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
        mark.set_color_scheme(color_options.scheme)
        mark(svg, x, y)
 
    if symbol_options.legend:
        for mark in marks:
            if hasattr(mark, "_labels"):
                symbol_legend(svg, mark._labels, margin.left, margin.top, color_options.scheme)
                break
    
    return svg
