from collections.abc import Callable
from detroit.selection.selection import Selection

import detroit as d3

from .style import Style
from ..domain import domain
from ..scaler import Scaler, determine_scaler
from ..transformers import getter, Identity

class Line(Style):
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        fill: Callable | str | None = None,
        fill_opacity: float = 1.,
        stroke: Callable | str | None = None,
        stroke_width: float = 1.,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
        self._data = data
        self.x_label = None if callable(x) else str(x)
        self.y_label = None if callable(y) else str(y)
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

        Style.__init__(
            self,
            data=data,
            default_fill="none",
            default_stroke="black",
            fill=fill,
            fill_opacity=fill_opacity,
            stroke=stroke,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            stroke_dasharray=stroke_dasharray,
            opacity=opacity,
        )

    def __call__(
        self,
        svg: Selection,
        x: Callable,
        y: Callable,
    ):
        line = (
            d3.line()
            .x(
                (lambda d: x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINOUS
                else (lambda d: x(self._x(d).timestamp()))
            )
            .y(lambda d: y(self._y(d)))
        )

        (
            svg.append("g")
            .attr("class", "line")
            .append("path")
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
            .attr("d", line(self._data))
        )
