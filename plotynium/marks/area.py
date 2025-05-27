from collections.abc import Callable

import detroit as d3
from detroit.selection import Selection

from ..context import Context
from ..domain import domain, reduce
from ..scaler import Scaler, determine_scaler
from ..transformers import Constant, getter
from ..types import Data, Index, T
from .mark import Mark
from .style import Style


class AreaY(Style[T], Mark):
    """
    Marker for drawing areas defined by y positions.

    Parameters
    ----------
    data : list[T]
        List where point coordinates are stored.
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[[T], Data] | str | None
        Y accessor function or key value when area begins from `y = 0` (do not specify
        `y1` or `y2` if you choose this argument).
    y1 : Callable[[T], Data] | str | None
        Y accessor function or key value for y positions for the bottom area's part (do
        not specify `y` argument if you choose the this argument).
    y2 : Callable[[T], Data] | str | None
        Y accessor function or key value for y positions for the top area's part (do
        not specify `y` argument if you choose the this argument).
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

    Raises
    ------
    RuntimeError
        When incoherence found between 'y0' and 'y1' domains.
    ValueError
        When 'y' is undefined or 'y1' and 'y2' are undefined.
    """

    def __init__(
        self,
        data: list[T],
        x: Callable[[T], Data] | Index | str | None = None,
        y: Callable[[T], Data] | Index | str | None = None,
        y1: Callable[[T], Data] | Index | str | None = None,
        y2: Callable[[T], Data] | Index | str | None = None,
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.0,
        stroke_opacity: float = 1.0,
        stroke_dasharray: str | None = None,
        opacity: float = 1.0,
    ):
        Mark.__init__(self)
        self._data = data
        self.x_label = x if isinstance(x, str) else None
        self.y_label = y if isinstance(y, str) else None
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        if y1 is not None and y2 is not None:
            self._y0 = getter(y1)
            self._y1 = getter(y2)
        elif y1 is None and y2 is None:
            self._y1 = getter(y or 1)
            self._y0 = Constant(0)
        else:
            raise ValueError(
                "'y' must be specified or 'y1' and 'y2' must be specified."
            )

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

    def apply(self, svg: Selection, ctx: Context):
        """
        Add an area defined by y values on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx : Context
            Context
        """
        area = (
            d3.area()
            .x(
                (lambda d: ctx.x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINUOUS
                else (lambda d: ctx.x(self._x(d).timestamp()))
            )
            .y0(lambda d: ctx.y(self._y0(d)))
            .y1(lambda d: ctx.y(self._y1(d)))
        )

        area = (
            svg.append("g")
            .attr("class", "area")
            .append("path")
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
            .attr("d", area(self._data))
        )

        if self._opacity != 1.0:
            area.attr("opacity", self._opacity)
        if self._stroke_opacity != 1.0:
            area.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_dasharray is not None:
            area.attr("stroke-dasharray", self._stroke_dasharray)
        if self._fill_opacity != 1.0:
            area.attr("fill-opacity", self._fill_opacity)
