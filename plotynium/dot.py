from collections.abc import Callable
from operator import itemgetter

import detroit as d3
from detroit.selection.selection import Selection

def getter(value):
    return value if callable(value) else itemgetter(value)

class ColorMaker:
    def __init__(self, data, value):
        self.value = getter(value)
        self.color_scheme = d3.interpolate_turbo
        self._color = d3.scale_sequential(
            [
                min(map(itemgetter(value), data)),
                max(map(itemgetter(value), data)),
            ],
            self.color_scheme
        )

    def __call__(self, d):
        d = self.value(d)
        return self._color(d)

class Dot:
    def __init__(
        self,
        data: list, 
        x: str | None = None,
        y: str | None = None,
        stroke: Callable | str | None = None,
        fill: Callable | str | None = None,
        r: Callable | float | None = None,
    ):
        self.data = data
        self.x = getter(x or 0)
        self.y = getter(y or 1)
        self.stroke = ColorMaker(data, stroke or "black")
        self.fill = "none" # ColorMaker(data, fill or "none")
        self.r = 3

    def __call__(
        self,
        svg: Selection,
        width: int,
        height: int,
        margin: tuple[int, int, int, int]
    ):

        (
            svg.append("g")
            .attr("fill", self.fill)
            .attr("stroke-width", 1.5)
            .select_all("circle")
            .data(self.data)
            .join("circle")
            .attr("transform", lambda d: f"translate({x(self.x(d))}, {y(self.y(d))})")
            .attr("stroke", self.stroke)
            .attr("r", 3)
        )

        (
            svg.append("g")
            .attr("transform", f"translate(0, {height - margin.bottom})")
            .call(d3.axis_bottom(x))
            .call(lambda g: g.select(".domain").remove())
            .call(
                lambda g: g.append("text")
                .attr("x", width - margin.right)
                .attr("y", -4)
                .attr("fill", "#000")
                .attr("font-weight", "bold")
                .attr("text-anchor", "end")
                .text("Component 1")
            )
        )

        (
            svg.append("g")
            .attr("transform", f"translate({margin.left}, 0)")
            .call(d3.axis_left(y))
            .call(lambda g: g.select(".domain").remove())
            .call(
                lambda g: g.select(".tick:last-of-type")
                .select("text")
                .clone()
                .attr("x", 4)
                .attr("text-anchor", "start")
                .attr("font-weight", "bold")
                .text("Component 2")
            )
        )
