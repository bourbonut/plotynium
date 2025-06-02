from collections.abc import Callable

from detroit.selection import Selection

from ..context import Context
from ..domain import domain
from ..scaler import determine_scaler
from ..transformers import Constant, Identity, Symbol, getter
from ..types import Data, T
from .mark import Mark
from .style import Style


def center(scale: Callable) -> Callable[[T], float]:
    """
    Centralize tick coordinates if `scale` argument has a `get_bandwidth`.

    Parameters
    ----------
    scale : Callable
        Scaler from `detroit`.

    Returns
    -------
    Callable[[T], float]
        Modified scaler.
    """
    if hasattr(scale, "get_bandwidth"):
        offset = max(0, scale.get_bandwidth()) / 2

        def scale_center(d):
            return scale(d) + offset

        return scale_center
    return scale


class Dot(Style[T], Mark):
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
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.5,
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

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

        self._r = r if callable(r) else Constant(r or 3)
        self._symbol = Symbol.try_init(data, symbol)

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

    def apply(self, svg: Selection, ctx: Context):
        """
        Add circles or symbols on the SVG content.

        Parameters
        ----------
        svg : Selection
            SVG content
        ctx : Context
            Context
        """
        self.set_colorscheme(ctx.color_scheme)
        self.set_labels(ctx.labels)
        x = center(ctx.x)
        y = center(ctx.y)
        if isinstance(self._symbol, Identity):
            group = svg.append("g").attr("class", "dots")

            if self._opacity != 1.0:
                group.attr("opacity", self._opacity)
            if self._stroke_opacity != 1.0:
                group.attr("stroke-opacity", self._stroke_opacity)
            if self._stroke_dasharray is not None:
                group.attr("stroke-dasharray", self._stroke_dasharray)
            if self._fill_opacity != 1.0:
                group.attr("fill-opacity", self._fill_opacity)

            (
                group.select_all("circle")
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
            group = svg.append("g").attr("class", "dots")

            if self._opacity != 1.0:
                group.attr("opacity", self._opacity)
            if self._stroke_opacity != 1.0:
                group.attr("stroke-opacity", self._stroke_opacity)
            if self._stroke_dasharray is not None:
                group.attr("stroke-dasharray", self._stroke_dasharray)
            if self._fill_opacity != 1.0:
                group.attr("fill-opacity", self._fill_opacity)

            (
                group.select_all("symbol")
                .data(self._data)
                .join("g")
                .attr(
                    "transform",
                    lambda d: f"translate({x(self._x(d))}, {y(self._y(d))})",
                )
                .append("path")
                .attr("d", self._symbol)
                .attr("stroke", self._stroke)
                .attr("fill", self._fill)
                .attr("stroke-width", self._stroke_width)
            )
            ctx.update_symbol_mapping(self._symbol.get_mapping())
        ctx.update_color_mapping(
            self._stroke.get_mapping(),
            self._fill.get_mapping(),
        )
