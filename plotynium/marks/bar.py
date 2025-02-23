from collections.abc import Callable
from detroit.selection.selection import Selection

import detroit as d3

from .style import Style
from ..options import SortOptions, init_options
from ..utils import getter
from ..domain import domain
from ..scaler import Scaler, determine_scaler

class BarY(Style):
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        sort: SortOptions | dict | None = None,
        fill: Callable | str | None = None,
        fill_opacity: float = 1.,
        stroke: Callable | str | None = None,
        stroke_width: float = 1.,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
        sort = init_options(sort, SortOptions)
        if sort.by != "":
            data = sorted(data, key=getter(sort.by))
            if sort.descending:
                data = list(reversed(data))

        self._data = data
        self.x_label = None if callable(x) else x
        self.y_label = None if callable(y) else y
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

        Style.__init__(
            self,
            data=data,
            default_fill="black",
            default_stroke="none",
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
        **kwargs,
    ):
        (
            svg.append("g")
            .attr("class", "bars")
            .select_all()
            .data(self._data)
            .join("rect")
            .attr("x", lambda d: x(self._x(d)))
            .attr("y", lambda d: y(self._y(d)))
            .attr("height", lambda d: y(0) - y(self._y(d)))
            .attr("width", x.bandwidth)
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
        )
