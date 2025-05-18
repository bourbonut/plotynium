from functools import reduce
from itertools import accumulate
from operator import iadd, itemgetter

from detroit.selection import Selection

from .string_widths import STRING_WIDTHS


class DiscreteLegend:
    def discrete_color_legend(self, svg: Selection):
        """
        Adds to the SVG input, a legend described by labels associated with
        rectangles

        Parameters
        ----------
        svg : Selection
            SVG on which the legend will be added
        """
        square_size = 15
        ratio = self._font_size / 2
        labels = list(map(itemgetter(0), self._color_mapping))
        lengths = [
            reduce(iadd, [STRING_WIDTHS.get(char, 1) for char in str(label)], 0)
            for label in labels
        ]
        offsets = [0] + [2 * square_size + length * ratio for length in lengths[:-1]]
        offsets = list(accumulate(offsets))
        margin_top = self._properties.margin.top
        margin_left = self._properties.margin.left

        legend = (
            svg.append("g")
            .attr("class", "legend")
            .attr("transform", f"translate({margin_left}, {margin_top})")
            .select_all("legend")
            .data(self._color_mapping)
            .enter()
        )

        g = legend.append("g").attr(
            "transform", lambda _, i: f"translate({offsets[i]}, 0)"
        )

        (
            g.append("rect")
            .attr("x", -square_size / 2)
            .attr("y", -square_size / 2)
            .attr("width", square_size)
            .attr("height", square_size)
            .attr("fill", lambda d: d[1])
            .style("stroke", "none")
        )

        (
            g.append("text")
            .attr("x", square_size * 0.5 + 4)
            .attr("y", self._font_size // 3)
            .text(lambda d: str(d[0]))
            .style("fill", "currentColor")
            .style("font-size", self._font_size)
        )
