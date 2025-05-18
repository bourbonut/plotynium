from functools import reduce
from itertools import accumulate
from operator import iadd, itemgetter

from detroit.selection import Selection

from .string_widths import STRING_WIDTHS


class SymbolLegend:
    def symbol_legend(self, svg: Selection):
        """
        Adds to the SVG input, a legend described by labels associated with symbols

        Parameters
        ----------
        svg : Selection
            SVG on which the legend will be added
        """
        data = [
            (label, color, symbol)
            for (label, color), (label, symbol) in zip(
                self._color_mapping, self._symbol_mapping
            )
        ]
        labels = list(map(itemgetter(0), data))
        if not labels:
            return
        symbol_size = self._symbol_size
        ratio = self._font_size / 2
        lengths = [
            reduce(iadd, [STRING_WIDTHS.get(char, 1) for char in str(label)], 0)
            for label in labels
        ]
        offsets = [0] + [6 * symbol_size + length * ratio for length in lengths[:-1]]
        offsets = list(accumulate(offsets))
        margin_top = self._properties.margin.top
        margin_left = self._properties.margin.left

        legend = (
            svg.append("g")
            .attr("class", "legend")
            .attr("transform", f"translate({margin_left}, {margin_top})")
            .select_all("legend")
            .data(data)
            .enter()
        )

        g = legend.append("g").attr(
            "transform", lambda _, i: f"translate({offsets[i]}, 0)"
        )

        (
            g.append("path")
            .attr("d", lambda d: d[2])
            .style("stroke", lambda d: d[1])
            .style("fill", "none")
        )

        (
            g.append("text")
            .attr("x", symbol_size * 1.5 + 4)
            .attr("y", self._font_size // 3)
            .text(lambda d: str(d[0]))
            .style("fill", "currentColor")
            .style("font-size", self._font_size)
        )
