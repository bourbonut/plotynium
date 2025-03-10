from itertools import accumulate
from functools import reduce
from operator import iadd
import detroit as d3
from detroit.selection.selection import Selection
from .schemes import Scheme
from .string_widths import STRING_WIDTHS
from .interpolations import Interpolation

def discrete_color_legend(
    svg: Selection,
    labels: list,
    margin_left: int,
    margin_top: int,
    scheme: Interpolation | Scheme,
    font_size: int = 12,
):
    """
    Adds to the SVG input, a legend described by labels associated with rectangles

    Parameters
    ----------
    svg : Selection
        SVG on which the legend will be added
    labels : list
        Labels to make the legend
    margin_left : int
        Margin left value
    margin_top : int
        Margin top value
    scheme : Interpolation | Scheme
        Color scheme
    font_size : int
        Font size of labels
    """
    nb_columns = len(labels)
    rect_size = 15
    ratio = font_size / 2
    lengths = [reduce(iadd, [STRING_WIDTHS.get(char, 1) for char in str(label)], 0) for label in labels]
    offsets = [0] + [2 * rect_size + length * ratio for length in lengths[:-1]]
    offsets = list(accumulate(offsets))

    color = d3.scale_sequential([0, len(labels) - 1], scheme)

    legend = (
        svg.append("g")
        .attr("class", "legend")
        .attr("transform", f"translate({margin_left // 2}, {margin_top // 2})")
        .select_all("legend")
        .data(labels)
        .enter()
    )

    g = (
        legend.append("g")
        .attr("transform", lambda _, i: f"translate({offsets[i]}, 0)")
    )

    (
        g.append("rect")
        .attr("x", -rect_size / 2)
        .attr("y", -rect_size / 2)
        .attr("width", rect_size)
        .attr("height", rect_size)
        .attr("fill", lambda _, i: color(i))
        .style("stroke", "none")
    )

    (
        g.append("text")
        .attr("x", rect_size * 0.5 + 4)
        .attr("y", font_size // 3)
        .text(lambda d: str(d))
        .style("fill", "currentColor")
        .style("font-size", font_size)
    )
