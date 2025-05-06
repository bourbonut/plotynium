from typing import Literal
from detroit.selection import Selection
from collections.abc import Callable
from typing import Generic

from ..transformers import Identity, Constant
from ..getter import getter
from ..domain import domain
from ..scaler import determine_scaler
from ..types import Data, T

class AxisX(Generic[T]):
    """
    Marker for making an X axis.

    Parameters
    ----------
    data : list[T] | None
        List of data for making X axis
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[..., float] | str | None
        Y accessor function or key value
    anchor : Literal["top", "bottom"]
        Anchor location, where `"top"` orientates ticks up and sets the axis position
        on the top of the plot whereas `"bottom"` orientates ticks down and sets the
        axis position on the bottom.
    label : str | None
        Label of the x axis.
    fill : str | None
        Fill color value.
    tick_rotate : float
        Tick rotation value.
    tick_size : int
        Tick size value.
    tick_format : Callable[[T], str] | None
        Tick format function which takes a data and returns a string.
    stroke : str | None
        Stroke color value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_width : float
        Stroke width value.
    """
    def __init__(
        self,
        data: list[T] | None = None,
        x: Callable[[T], Data] | str | None = None,
        y: Callable[..., float] | str | None = None,
        anchor: Literal["top", "bottom"] = "bottom",
        label: str | None = None,
        fill: str | None = None,
        tick_rotate: float = 0.,
        tick_size: int = 6,
        tick_format: Callable[[T], str] | None = None,
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
        Add X axis to SVG content

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
            tx = (x.get_range()[0] + x.get_range()[1]) // 2
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

class AxisY(Generic[T]):
    """
    Marker for making an Y axis.

    Parameters
    ----------
    data : list[T] | None
        List of data for making Y axis
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[..., float] | str | None
        Y accessor function or key value
    anchor : Literal["left", "right"]
        Anchor location, where `"left"` orientates ticks on left side and sets the axis
        position on the left of the plot whereas `"right"` orientates ticks on right
        side and sets the axis position on the right.
    label : str | None
        Label of the x axis.
    fill : str | None
        Fill color value.
    tick_rotate : float
        Tick rotation value.
    tick_size : int
        Tick size value.
    tick_format : Callable[[T], str] | None
        Tick format function which takes a data and returns a string.
    stroke : str | None
        Stroke color value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_width : float
        Stroke width value.
    """
    def __init__(
        self,
        data: list[T] | None = None,
        x: Callable[..., float] | str | None = None,
        y: Callable[[T], Data] | str | None = None,
        anchor: Literal["left", "right"] = "left",
        label: str | None = None,
        fill: str | None = None,
        tick_rotate: float = 0.,
        tick_size: int = 6,
        tick_format: Callable[[T], str] | None = None,
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
        Add Y axis to SVG content

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
            tx = -(y.get_range()[0] + y.get_range()[1]) // 2
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
                .attr("transform", "matrix(0 -1 1 0 0.5 0)")
                .append("text")
                .attr("transform", f"translate({tx}, {ty})")
                .text(self._label)
            )
