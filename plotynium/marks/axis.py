from typing import Literal
from detroit.selection.selection import Selection
from collections.abc import Callable
from inspect import signature

import detroit as d3

from ..utils import getter, Identity, Constant
from ..domain import domain
from ..scaler import determine_scaler

class AxisX:
    def __init__(
        self,
        data: list | None = None,
        x: Callable | str | None = None,
        y: Callable[..., float] | str | None = None,
        anchor: Literal["top", "bottom"] = "bottom",
        label: str | None = None,
        fill: str | None = None,
        tick_rotate: float = 0.,
        tick_size: int = 6,
        tick_format: Callable | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 1.,
        stroke_width: float = 1,
    ):
        self._data = data or d3.ticks(0, 1, 10)
        self._x = x or Identity()
        self._y = None if y is None else getter(y)
        self._anchor = anchor
        self._label = label
        self._fill = fill or "inherit"
        self._tick_rotate = tick_rotate
        self._tick_size = tick_size
        self._tick_format = tick_format if callable(tick_format) else Identity()
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width

        self.x_label = self._label
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
        dy = height - margin_bottom if self._anchor == "bottom" else margin_top
        y = self._y or Constant(dy)
        dir = -1 if self._anchor == "top" else 1

        if hasattr(x, "bandwidth"):
            offset = x.bandwidth / 2
        else:
            offset = 0

        ticks = (
            svg.append("g")
            .attr("aria-label", "x-axis tick")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .select_all("path")
            .data(self._data)
            .join("path")
            .attr("transform", lambda d: f"translate({x(d) + offset}, {y(d)})")
            .attr("d", f"M0,0L0,{dir * self._tick_size}")
        )
        if self._stroke_opacity != 1.:
            ticks.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_width != 1.:
            ticks.attr("stroke-width", self._stroke_width)

        (
            svg.append("g")
            .attr("aria-label", "x-axis tick label")
            .attr("transform", f"translate(0, {dir * (self._tick_size + 2.5)})")
            .attr("text-anchor", "middle")
            .attr("fill", self._fill)
            .select_all("text")
            .data(self._data)
            .join("text")
            .attr("y", "0.71em" if self._anchor == "bottom" else "0px")
            .attr("transform", lambda d: f"translate({x(d) + offset}, {y(d)})")
            .text(lambda d: str(self._tick_format(d)))
        )

        if self._label is not None:
            tx = (x.range[0] + x.range[1]) // 2
            ty = (
                height - margin_bottom // 4
                if self._anchor == "bottom" else
                margin_top // 4
            )
            (
                svg.append("g")
                .attr("aria-label", "x-axis label")
                .attr("text-anchor", "middle")
                .attr("fill", self._fill)
                .attr("transform", f"translate(0.5, 0)")
                .append("text")
                .attr("transform", f"translate({tx}, {ty})")
                .text(self._label)
            )

class AxisY:
    def __init__(
        self,
        data: list | None = None,
        x: Callable[..., float] | str | None = None,
        y: Callable | str | None = None,
        anchor: Literal["left", "right"] = "left",
        label: str | None = None,
        fill: str | None = None,
        tick_rotate: float = 0.,
        tick_size: int = 6,
        tick_format: Callable | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 1.,
        stroke_width: float = 1,
    ):
        self._data = data or d3.ticks(0, 1, 10)
        self._x = None if x is None else getter(x)
        self._y = y or Identity()
        self._anchor = anchor
        self._label = label
        self._fill = fill or "inherit"
        self._tick_rotate = tick_rotate
        self._tick_size = tick_size
        self._tick_format = tick_format if callable(tick_format) else Identity()
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width

        self.x_label = None
        self.y_label = self._label
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
        dx = margin_left if self._anchor == "left" else width - margin_right
        x = self._x or Constant(dx)
        dir = -1 if self._anchor == "left" else 1

        if hasattr(y, "bandwidth"):
            offset = y.bandwidth / 2
        else:
            offset = 0

        ticks = (
            svg.append("g")
            .attr("aria-label", "y-axis tick")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .select_all("path")
            .data(self._data)
            .join("path")
            .attr("transform", lambda d: f"translate({x(d)}, {y(d) + offset})")
            .attr("d", f"M0,0L{dir * self._tick_size},0")
        )

        if self._stroke_opacity != 1.:
            ticks.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_width != 1.:
            ticks.attr("stroke-width", self._stroke_width)

        (
            svg.append("g")
            .attr("aria-label", "y-axis tick label")
            .attr("transform", f"translate({dir * (self._tick_size + 2.5)}, 0)")
            .attr("text-anchor", "end" if self._anchor == "left" else "start")
            .attr("fill", self._fill)
            .select_all("text")
            .data(self._data)
            .join("text")
            .attr("y", "0.32em")
            .attr("transform", lambda d: f"translate({x(d)}, {y(d) + offset})")
            .text(lambda d: str(self._tick_format(d)))
        )

        if self._label is not None:
            tx = -(y.range[0] + y.range[1]) // 2
            ty = (
                margin_left // 4
                if self._anchor == "left" else
                width - margin_right //  4
            )
            (
                svg.append("g")
                .attr("aria-label", "y-axis label")
                .attr("text-anchor", "middle")
                .attr("fill", self._fill)
                .attr("transform", f"matrix(0 -1 1 0 0.5 0)")
                .append("text")
                .attr("transform", f"translate({tx}, {ty})")
                .text(self._label)
            )
