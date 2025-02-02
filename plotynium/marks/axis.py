from typing import Literal
from detroit.selection.selection import Selection
from collections.abc import Callable
from inspect import signature

import detroit as d3

from ..utils import getter, Identity, Constant

class AxisX:
    def __init__(
        self,
        data: list | None = None,
        y: Callable[..., float] | str | None = None,
        anchor: Literal["top", "bottom"] = "bottom",
        label: str | None = None,
        label_anchor: Literal["center", "left", "right"] = "center",
        tick_rotate: float = 0.,
        tick_size: int = 6,
        tick_format: Callable | None = None,
        color: str | None = None,
        stroke: str | None = None,
        stroke_opacity: float = 1.,
        stroke_width: int = 1,
    ):
        self._data = data or d3.ticks(0, 1, 10)
        self._y = None if y is None else getter(y)
        self._anchor = anchor
        self._label = label
        self._label_anchor = label_anchor
        self._tick_rotate = tick_rotate
        self._tick_size = tick_size
        self._tick_format = Identity()
        self._color = color or "currentColor"
        self._stroke = stroke or "currentColor"
        self._stroke_opacity = stroke_opacity
        self._stroke_width = stroke_width

    def __call__(
        self,
        svg: Selection,
        x: Callable,
        y: Callable,
        height: int,
        margin_bottom: int,
        margin_left: int,
    ):
        y = self._y or Constant(height - margin_bottom)
        if callable(self._tick_format):
            text_func = self._tick_format
        else:
            text_func = Identity()

        (
            svg.append("g")
            .attr("aria-label", "x-axis tick")
            .attr("transform", f"translate(0.5, 0)")
            .attr("stroke", self._stroke)
            .attr("fill", "none")
            .select_all("path")
            .data(self._data)
            .join("path")
            .attr("transform", lambda d: f"translate({x(d)}, {y(d)})")
            .attr("d", f"M0,0L0,{self._tick_size}")
        )

        # TODO: add center position
        (
            svg.append("g")
            .attr("aria-label", "x-axis tick label")
            .attr("transform", f"translate(0.5, 9.5)")
            .select_all("text")
            .data(self._data)
            .join("text")
            .attr("y", "0.71em")
            .attr("transform", lambda d: f"translate({x(d) - len(str(d) * 3)}, {y(d)})")
            .text(lambda d: str(d))
        )
