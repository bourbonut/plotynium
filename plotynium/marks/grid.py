from typing import Literal
from detroit.selection.selection import Selection
from collections.abc import Callable
from inspect import signature
from typing import Generic

import detroit as d3

from ..utils import getter, Identity, Constant
from ..domain import domain
from ..scaler import determine_scaler
from ..types import Data, T

class GridX(Generic[T]):
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
        self.legend_labels = None

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
        """
        Add vertical lines from x ticks.

        Parameters
        ----------
        svg : Selection
            SVG Content
        x : Callable
            X scaler from `plot` function
        y : Callable
            Y scaler from `plot` function
        height : int
            Height value
        margin_top : int
            Margin top value
        margin_bottom : int
            Margin bottom value
        **kwargs
            Additional keyword arguments not used
        """
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

class GridY(Generic[T]):
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
        self.legend_labels = None

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
        """
        Add horizontal lines from y ticks.

        Parameters
        ----------
        svg : Selection
            SVG Content
        x : Callable
            X scaler from `plot` function
        y : Callable
            Y scaler from `plot` function
        width : int
            Width value
        margin_left : int
            Margin left value
        margin_right : int
            Margin right value
        **kwargs
            Additional keyword arguments not used
        """
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
