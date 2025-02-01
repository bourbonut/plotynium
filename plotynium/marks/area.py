from collections.abc import Callable
from detroit.selection.selection import Selection

import detroit as d3

from .style import Style
from ..domain import domain, reduce
from ..scaler import determine_scaler, Scaler
from ..options import SortOptions
from ..transformers import getter, Identity

class AreaY(Style):
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        y1: Callable | str | None = None,
        y2: Callable | str | None = None,
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

        if y is not None:
            self._y1 = getter(y or 1)
            self._y0 = Identity(0)
        elif y1 is not None or y2 is not None:
            self._y0 = getter(y1)
            self._y1 = getter(y2)
        else:
            raise ValueError("'y' must be specified or 'y1' and 'y2' must be specified.")

        self.x_domain = domain(self._data, self._x)
        y0_domain = domain(self._data, self._y0)
        y1_domain = domain(self._data, self._y1)

        self.x_scaler_type = determine_scaler(self._data, self._x)
        y0_scaler_type = determine_scaler(self._data, self._y0)
        y1_scaler_type = determine_scaler(self._data, self._y1)
        if y0_scaler_type == y1_scaler_type:
            self.y_scaler_type = y0_scaler_type
        else:
            raise RuntimeError(
                "Incoherence between 'y0' and 'y1' domains "
                f"(found y0 domain: {y0_domain} and y1 domain : {y1_domain})"
            )

        self.y_domain = reduce([y0_domain, y1_domain])

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
    ):
        area = (
            d3.area()
            .x(
                (lambda d: x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINOUS
                else (lambda d: x(self._x(d).timestamp()))
            )
            .y0(lambda d: y(self._y0(d)))
            .y1(lambda d: y(self._y1(d)))
        )

        (
            svg.append("g")
            .attr("class", "area")
            .append("path")
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
            .attr("d", area(self._data))
        )

