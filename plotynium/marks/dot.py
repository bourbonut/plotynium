from collections.abc import Callable
from detroit.selection.selection import Selection
from detroit.scale.band import ScaleBand

import detroit as d3

from .style import Style
from ..domain import domain
from ..scaler import Scaler, determine_scaler
from ..utils import getter, Constant, Symbol

def center(scale):
    if isinstance(scale, ScaleBand):
        offset = max(0, scale.bandwidth) / 2
        def scale_center(d):
            return scale(d) + offset
        return scale_center
    return scale

class Dot(Style):
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        r: Callable | float | None = None,
        symbol: Callable | float | None = None,
        fill: Callable | str | None = None,
        fill_opacity: float = 1.,
        stroke: Callable | str | None = None,
        stroke_width: float = 1.5,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
        self._data = data
        self.x_label = None if callable(x) else x
        self.y_label = None if callable(y) else y
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

        self._r = r if callable(r) else Constant(r or 3)
        self._symbol = Symbol.try_init(data, symbol)
        self._labels = self._symbol._labels if isinstance(self._symbol, Symbol) else []

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
        **kwargs,
    ):
        x = center(x)
        y = center(y)
        if self._symbol is None:
            (
                svg.append("g")
                .attr("class", "dots")
                .select_all("circle")
                .data(self._data)
                .join("circle")
                .attr("cx", lambda d: x(self._x(d)))
                .attr("cy", lambda d: y(self._y(d)))
                .attr("stroke", self._stroke)
                .attr("fill", self._fill)
                .attr("stroke-width", self._stroke_width)
                .attr("r", self._r)
            )
        else:
            (
                svg.append("g")
                .attr("class", "dots")
                .select_all("symbol")
                .data(self._data)
                .join("g")
                .attr("transform", lambda d: f"translate({x(self._x(d))}, {y(self._y(d))})")
                .append("path")
                .attr("d", self._symbol)
                .attr("stroke", self._stroke)
                .attr("fill", self._fill)
                .attr("stroke-width", self._stroke_width)
            )

