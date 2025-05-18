from collections.abc import Callable
from typing import Generic

import detroit as d3
from detroit.selection import Selection

from ..context import Context
from ..domain import domain
from ..scaler import determine_scaler
from ..transformers import Constant, Identity
from ..types import Data, T
from .mark import Mark


class GridX(Generic[T], Mark):
    """
    Marker for adding vertical lines from x ticks.

    Parameters
    ----------
    data : list[T]
        List of x positions where vertical lines will be placed.
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y1 : Callable[[T], Data] | str | None
        Y accessor function or key value for tail coordinates of the lines
    y2 : Callable[[T], Data] | str | None
        Y accessor function or key value for head coordinates of the lines
    stroke : Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `stroke` attribute.
    stroke_width : float
        Stroke width value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_dasharray : str | None
        Stroke dasharray value.
    """

    def __init__(
        self,
        data: list[T] | None = None,
        x: Callable[[T], Data] | str | None = None,
        y1: Callable[[T], Data] | None = None,
        y2: Callable[[T], Data] | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 0.1,
        stroke_width: float = 1,
        stroke_dasharray: str | None = None,
    ):
        Mark.__init__(self)
        self._data = data or d3.ticks(0, 1, 10)
        self._x = x or Identity()
        self._y1 = y1
        self._y2 = y2
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray

        self.x_domain = domain(self._data, self._x)
        self.x_scaler_type = determine_scaler(self._data, self._x)

    def apply(self, svg: Selection, ctx: Context):
        """
        Add vertical lines from x ticks.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx: Context
            Context
        """
        height = ctx.height
        margin_top = ctx.margin.top
        margin_bottom = ctx.margin.bottom
        y1 = self._y1 or Constant(margin_top)
        y2 = self._y2 or Constant(height - margin_bottom)
        g = svg.append("g").attr("aria-label", "x-grid").attr("stroke", self._stroke)
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
            .attr("x1", lambda d: ctx.x(d))
            .attr("x2", lambda d: ctx.x(d))
            .attr("y1", y1)
            .attr("y2", y2)
        )


class GridY(Generic[T], Mark):
    """
    Marker for adding horizontal lines from y ticks.

    Parameters
    ----------
    data : list[T]
        List of y positions where horizontal lines will be placed.
    x1 : Callable[[T], Data] | str | None
        X accessor function or key value for tail coordinates of the lines
    x2 : Callable[[T], Data] | str | None
        X accessor function or key value for head coordinates of the lines
    y : Callable[[T], Data] | str | None
        Y accessor function or key value
    stroke : Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `stroke` attribute.
    stroke_width : float
        Stroke width value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_dasharray : str | None
        Stroke dasharray value.
    """

    def __init__(
        self,
        data: list[T] | None = None,
        x1: Callable[[T], Data] | None = None,
        x2: Callable[[T], Data] | None = None,
        y: Callable[[T], Data] | str | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 0.1,
        stroke_width: float = 1,
        stroke_dasharray: str | None = None,
    ):
        Mark.__init__(self)
        self._data = data or d3.ticks(0, 1, 10)
        self._x1 = x1
        self._x2 = x2
        self._y = y or Identity()
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray

        self.y_domain = domain(self._data, self._y)
        self.y_scaler_type = determine_scaler(self._data, self._y)

    def apply(self, svg: Selection, ctx: Context):
        """
        Add horizontal lines from y ticks.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx : Context
            Context
        """
        width = ctx.width
        margin_right = ctx.margin.right
        margin_left = ctx.margin.left
        x1 = self._x1 or Constant(margin_left)
        x2 = self._x2 or Constant(width - margin_right)
        g = svg.append("g").attr("aria-label", "y-grid").attr("stroke", self._stroke)
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
            .attr("x1", x1)
            .attr("x2", x2)
            .attr("y1", lambda d: ctx.y(d))
            .attr("y2", lambda d: ctx.y(d))
        )
