from collections.abc import Callable

import detroit as d3
from detroit.selection import Selection

from ..context import Context
from ..scaler import Scaler, determine_scaler
from ..transformers import Identity, getter
from ..types import T
from .mark import Mark
from .style import Style


class RuleX(Style[T], Mark):
    """
    Marker for adding vertical lines given a list of x positions

    Parameters
    ----------
    x : list[T]
        List of x positions where vertical lines will be placed.
    fill : Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `fill` attribute.
    fill_opacity : float
        Fill opacity value included in [0, 1].
    stroke : Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `stroke` attribute.
    stroke_width : float
        Stroke width value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_dasharray : str | None
        Stroke dasharray value.
    opacity : float
        General opacity value included in [0, 1].
    """

    def __init__(
        self,
        x: list[T],
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.5,
        stroke_opacity: float = 1.0,
        stroke_dasharray: str | None = None,
        opacity: float = 1.0,
    ):
        Mark.__init__(self)
        self._values = list(x)
        self._x = getter(0)
        self._y = getter(1)

        self.x_domain = [min(self._values), max(self._values)]
        self.x_scaler_type = determine_scaler(self._values, Identity())

        Style.__init__(
            self,
            data=[],
            default_fill="none",
            default_stroke="currentColor",
            fill=fill,
            fill_opacity=fill_opacity,
            stroke=stroke,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            stroke_dasharray=stroke_dasharray,
            opacity=opacity,
        )

    def apply(self, svg: Selection, ctx: Context):
        """
        Add horizontal lines on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx: Context
            Context
        """
        line = (
            d3.line()
            .x(
                (lambda d: ctx.x(self._x(d).timestamp()))
                if self.x_scaler_type == Scaler.TIME
                else lambda d: ctx.x(self._x(d))
            )
            .y(lambda d: ctx.y(self._y(d)))
        )
        values = [
            [[v, ctx.y.get_domain()[0]], [v, ctx.y.get_domain()[1]]]
            for v in self._values
        ]
        group = svg.append("g").attr("class", "rule")

        if self._opacity != 1.0:
            group.attr("opacity", self._opacity)
        if self._stroke_opacity != 1.0:
            group.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_dasharray is not None:
            group.attr("stroke-dasharray", self._stroke_dasharray)
        if self._fill_opacity != 1.0:
            group.attr("fill-opacity", self._fill_opacity)

        (
            group.select_all("rule")
            .data(values)
            .join("path")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .attr("stroke-width", self._stroke_width)
            .attr("d", lambda d: line(d))
        )


class RuleY(Style[T], Mark):
    """
    Marker for adding horizontal lines given a list of y positions

    Parameters
    ----------
    y : list[T]
        List of y positions where horizontal lines will be placed.
    fill : Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `fill` attribute.
    fill_opacity : float
        Fill opacity value included in [0, 1].
    stroke : Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `stroke` attribute.
    stroke_width : float
        Stroke width value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_dasharray : str | None
        Stroke dasharray value.
    opacity : float
        General opacity value included in [0, 1].
    """

    def __init__(
        self,
        y: list[T],
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.5,
        stroke_opacity: float = 1.0,
        stroke_dasharray: str | None = None,
        opacity: float = 1.0,
    ):
        Mark.__init__(self)
        self._values = list(y)
        self._x = getter(0)
        self._y = getter(1)

        self.y_domain = [min(self._values), max(self._values)]
        self.y_scaler_type = determine_scaler(self._values, Identity())

        Style.__init__(
            self,
            data=[],
            default_fill="none",
            default_stroke="currentColor",
            fill=fill,
            fill_opacity=fill_opacity,
            stroke=stroke,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            stroke_dasharray=stroke_dasharray,
            opacity=opacity,
        )

    def apply(self, svg: Selection, ctx: Context):
        """
        Add horizontal lines on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx: Context
            Context
        """
        line = (
            d3.line()
            .x(lambda d: ctx.x(self._x(d)))
            .y(
                (lambda d: ctx.y(self._y(d).timestamp()))
                if self.y_scaler_type == Scaler.TIME
                else lambda d: ctx.y(self._y(d))
            )
        )
        values = [
            [[ctx.x.get_domain()[0], v], [ctx.x.get_domain()[1], v]]
            for v in self._values
        ]
        group = svg.append("g").attr("class", "rule")

        if self._opacity != 1.0:
            group.attr("opacity", self._opacity)
        if self._stroke_opacity != 1.0:
            group.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_dasharray is not None:
            group.attr("stroke-dasharray", self._stroke_dasharray)
        if self._fill_opacity != 1.0:
            group.attr("fill-opacity", self._fill_opacity)

        (
            group.select_all("rule")
            .data(values)
            .join("path")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .attr("stroke-width", self._stroke_width)
            .attr("d", lambda d: line(d))
        )
