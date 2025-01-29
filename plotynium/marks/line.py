from datetime import datetime
import detroit as d3
from detroit.selection.selection import Selection
from collections.abc import Callable
from ..transformers import getter, Identity, Color, Symbol, Maker
from ..domain import domain
from ..schemes import Scheme
from ..scaler import Scaler

class Line:
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        stroke: Callable | str | None = None,
        fill: Callable | str | None = None,
        stroke_width: float | int = 1,
    ):
        self._data = data
        self.x_label = None if callable(x) else str(x)
        self.y_label = None if callable(y) else str(y)
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain, self.x_scaler_type = domain(data, self._x)
        self.y_domain, self.y_scaler_type = domain(data, self._y)
        self._stroke = Color.try_init(data, stroke, Identity(stroke or "black"))
        self._fill = Color.try_init(data, fill, Identity(fill or "none"))
        self._stroke_width = stroke_width

    def set_color_scheme(self, scheme: Scheme):
        if scheme is None:
            return
        if isinstance(self._stroke, Maker):
            self._stroke.set_color_scheme(scheme)
        if isinstance(self._fill, Maker):
            self._fill.set_color_scheme(scheme)

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
            svg.append("path")
            .attr("class", "line")
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
            .attr("d", line(self._data))
        )
