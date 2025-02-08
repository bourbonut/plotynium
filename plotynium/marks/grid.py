from typing import Literal
from detroit.selection.selection import Selection
from collections.abc import Callable
from inspect import signature

import detroit as d3

from ..utils import getter, Identity, Constant
from ..domain import domain
from ..scaler import determine_scaler

class GridX:
    def __init__(
        self,
        data: list | None = None,
        x: Callable | str | None = None,
        y1: Callable | None = None,
        y2: Callable | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 0.1,
        stroke_width: float = 1,
        stroke_dasharray: str | None = None,
    ):
        self._data = data or d3.ticks(0, 1, 10)
        self._x = x or Identity()
        self._y1 = y1
        self._y2 = y2
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray

        self.x_label = None
        self.y_label = None
        self.x_domain = domain(self._data, self._x)
        self.y_domain = None
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = None

    def __call__(
        self,
        svg: Selection,
        x: Callable,
        y: Callable,
        height: int,
        margin_top: int,
        margin_bottom: int,
        **kwargs,
    ):
        y1 = self._y1 or Constant(margin_top)
        y2 = self._y2 or Constant(height - margin_bottom)
        g = (
            svg.append("g")
            .attr("aria-label", "x-grid")
            .attr("stroke", self._stroke)
        )
        if self._stroke_width:
            g.attr("stroke_width", self._stroke_width)
        if self._stroke_dasharray:
            g.attr("stroke-dasharray", self._stroke_dasharray)
        if self._stroke_opacity:
            g.attr("stroke-opacity", self._stroke_opacity)

        (
            g.select_all("line")
            .data(self._data)
            .join("line")
            .attr("x1", lambda d: x(d))
            .attr("x2", lambda d: x(d))
            .attr("y1", y1)
            .attr("y2", y2)
        )

class GridY:
    def __init__(
        self,
        data: list | None = None,
        x1: Callable | None = None,
        x2: Callable | None = None,
        y: Callable | str | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 0.1,
        stroke_width: float = 1,
        stroke_dasharray: str | None = None,
    ):
        self._data = data or d3.ticks(0, 1, 10)
        self._x1 = x1
        self._x2 = x2
        self._y = y or Identity()
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray

        self.x_label = None
        self.y_label = None
        self.x_domain = None
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = None
        self.y_scaler_type = determine_scaler(self._data, self._y)

    def __call__(
        self,
        svg: Selection,
        x: Callable,
        y: Callable,
        width: int,
        margin_left: int,
        margin_right: int,
        **kwargs,
    ):
        x1 = self._x1 or Constant(margin_left)
        x2 = self._x2 or Constant(width - margin_right)
        g = (
            svg.append("g")
            .attr("aria-label", "y-grid")
            .attr("stroke", self._stroke)
        )
        if self._stroke_width:
            g.attr("stroke_width", self._stroke_width)
        if self._stroke_dasharray:
            g.attr("stroke-dasharray", self._stroke_dasharray)
        if self._stroke_opacity:
            g.attr("stroke-opacity", self._stroke_opacity)

        g1 = (
            g.select_all("line")
            .data(self._data)
            .join("line")
            .attr("x1", x1)
            .attr("x2", x2)
            .attr("y1", lambda d: y(d))
            .attr("y2", lambda d: y(d))
        )
