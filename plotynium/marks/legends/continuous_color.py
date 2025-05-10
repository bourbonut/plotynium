from detroit.selection import Selection
import detroit as d3

class ContinuousLegend:
    def continuous_color_legend(self, svg: Selection):
        """
        Adds to the SVG input, a color gradient based on scheme and color values

        Parameters
        ----------
        svg : Selection
            SVG on which the legend will be added
        """
        width = 240
        rect_width = 2
        height = 10
        data = list(range(0, width, rect_width))
        (
            svg.append("g")
            .attr("aria-label", "legend gradient")
            .select_all("rect")
            .data(data)
            .join("rect")
            .attr("x", lambda d: d)
            .attr("y", 0)
            .attr("width", lambda _, i: rect_width + bool(i < (len(data) - 1)))
            .attr("height", height)
            .attr("fill", lambda d: self._scheme(d / width))
        )

        x = d3.scale_linear([0, 1], [0, width])
        tick_format = x.tick_format()
        (
            svg.append("g")
            .attr("aria-label", "legend tick")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .attr("stroke-width", self._stroke_width)
            .select_all("path")
            .data(d3.ticks(0, 1, 5))
            .join("path")
            .attr("transform", lambda d: f"translate({x(d)}, 0)")
            .attr("d", f"M0,0L0,{height + 5}")
        )

        (
            svg.append("g")
            .attr("aria-label", "legend tick label")
            .attr("transform", "translate(0, 5)")
            .attr("text-anchor", "middle")
            .attr("fill", self._fill)
            .select_all("text")
            .data(d3.ticks(0, 1, 5))
            .join("text")
            .attr("y", "0.71em")
            .attr("transform", lambda d: f"translate({x(d)}, {height})")
            .text(lambda d: str(tick_format(d)))
        )
