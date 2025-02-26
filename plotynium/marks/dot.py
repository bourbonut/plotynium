from collections.abc import Callable
from detroit.selection.selection import Selection
from detroit.scale.band import ScaleBand

import detroit as d3

from .style import Style
from ..domain import domain
from ..scaler import Scaler, determine_scaler
from ..utils import getter, Constant, Symbol
from ..types import Data, T

def center(scale: Callable) -> Callable[[T], float]:
    """
    Centralize tick coordinates if `scale` argument has a `bandwidth`.

    Parameters
    ----------
    scale : Callable
        Scaler from `detroit`.

    Returns
    -------
    Callable[[T], float]
        Modified scaler.
    """
    if isinstance(scale, ScaleBand):
        offset = max(0, scale.bandwidth) / 2
        def scale_center(d):
            return scale(d) + offset
        return scale_center
    return scale

class Dot(Style[T]):
    """
    Marker for add dots (as symbols or circles) given point coordinates.

    Parameters
    ----------
    data : list[T]
        List where points coordinates are stored.
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[[T], Data] | str | None
        Y accessor function or key value
    r : Callable[[T], float] | str | None
        Key value or function which returns circle radius given data.
    symbol : Callable[[T], str] | str | None
        Key value or function which returns symbol path given data.
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
        data: list[T],
        x: Callable[[T], Data] | str | None = None,
        y: Callable[[T], Data] | str | None = None,
        r: Callable[[T], float] | float | None = None,
        symbol: Callable[[T], str] | str | None = None,
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.,
        stroke: Callable[[T], str] | str | None = None,
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
        """
        Add circles or symbols on the SVG content.

        Parameters
        ----------
        svg : Selection
            SVG content
        x : Callable
            X scaler from `plot` function
        y : Callable
            Y scaler from `plot` function
        **kwargs
            Additional keyword arguments not used
        """
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
