import detroit as d3
from detroit.selection import Selection


class ContinuousLegend:
    def continuous_color_legend(self, svg: Selection):
        """
        Adds to the SVG input, a color gradient based on scheme and color values

        Parameters
        ----------
        svg : Selection
            SVG on which the legend will be added
        """
        margin_top = self._properties.margin.top
        margin_bottom = self._properties.margin.bottom
        margin_left = self._properties.margin.left
        margin_right = self._properties.margin.right
        width = self._properties.width
        height = self._properties.height
        thickness = height - margin_top - margin_bottom
        length = width - margin_right - margin_left
        rect_width = 2
        data = list(range(0, length, rect_width))

        legend = (
            svg.append("g")
            .attr("aria-label", "legend continuous")
            .attr("transform", f"translate({margin_left}, {margin_top})")
        )
        (
            legend.append("g")
            .attr("aria-label", "legend gradient")
            .select_all("rect")
            .data(data)
            .join("rect")
            .attr("x", lambda d: d)
            .attr("y", 0)
            .attr("width", lambda _, i: rect_width + bool(i < (len(data) - 1)))
            .attr("height", thickness)
            .attr("fill", lambda d: self._scheme(d / width))
        )

        domain = d3.extent(self._color_mapping, accessor=lambda d: d[0])
        x = d3.scale_linear(domain, [0, length]).nice()
        x_domain = x.get_domain()
        text_ticks = d3.ticks(x_domain[0], x_domain[1], 5)
        tick_format = x.tick_format()
        (
            legend.append("g")
            .attr("aria-label", "legend tick")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .attr("stroke-width", self._stroke_width)
            .select_all("path")
            .data(text_ticks)
            .join("path")
            .attr("transform", lambda d: f"translate({x(d)}, 0)")
            .attr("d", f"M0,0L0,{thickness + 5}")
        )

        (
            legend.append("g")
            .attr("aria-label", "legend tick label")
            .attr("transform", "translate(0, 5)")
            .attr("text-anchor", "middle")
            .attr("fill", self._fill)
            .select_all("text")
            .data(text_ticks)
            .join("text")
            .attr("y", "0.71em")
            .attr("transform", lambda d: f"translate({x(d)}, {thickness})")
            .text(lambda d: str(tick_format(d)))
        )
