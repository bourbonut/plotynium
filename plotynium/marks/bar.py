from collections.abc import Callable

from detroit.selection import Selection

from ..context import Context
from ..domain import domain
from ..options import SortOptions, init_options
from ..scaler import determine_scaler
from ..transformers import getter
from ..types import Data, T
from .mark import Mark
from .style import Style


class BarX(Style[T], Mark):
    """
    Marker for drawing horizontal bars based on given data.

    Parameters
    ----------
    data : list[T]
        List where bar information are stored.
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[[T], Data] | str | None
        Y accessor function or key value
    sort: SortOptions | dict | None
        Sort options used for ordering bars
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
        sort: SortOptions | dict | None = None,
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.0,
        stroke_opacity: float = 1.0,
        stroke_dasharray: str | None = None,
        opacity: float = 1.0,
    ):
        Mark.__init__(self)
        sort = init_options(sort, SortOptions)
        if sort.by != "":
            data = sorted(data, key=getter(sort.by))
            if sort.descending:
                data = list(reversed(data))

        self._data = data
        self.x_label = x if isinstance(x, str) else None
        self.y_label = y if isinstance(y, str) else None
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

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
        Add vertical bars on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx : Context
            Context
        """
        group = svg.append("g").attr("class", "bars")

        if self._opacity != 1.0:
            group.attr("opacity", self._opacity)
        if self._stroke_opacity != 1.0:
            group.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_dasharray is not None:
            group.attr("stroke-dasharray", self._stroke_dasharray)
        if self._fill_opacity != 1.0:
            group.attr("fill-opacity", self._fill_opacity)

        (
            group.select_all()
            .data(self._data)
            .join("rect")
            .attr("x", ctx.x(ctx.x.get_domain()[0]))
            .attr("y", lambda d: ctx.y(self._y(d)))
            .attr("width", lambda d: ctx.x(self._x(d)) - ctx.x(0))
            .attr("height", ctx.y.get_bandwidth())
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
        )


class BarY(Style[T], Mark):
    """
    Marker for drawing vertical bars based on given data.

    Parameters
    ----------
    data : list[T]
        List where bar information are stored.
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[[T], Data] | str | None
        Y accessor function or key value
    sort: SortOptions | dict | None
        Sort options used for ordering bars
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
        sort: SortOptions | dict | None = None,
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.0,
        stroke_opacity: float = 1.0,
        stroke_dasharray: str | None = None,
        opacity: float = 1.0,
    ):
        Mark.__init__(self)
        sort = init_options(sort, SortOptions)
        if sort.by != "":
            data = sorted(data, key=getter(sort.by))
            if sort.descending:
                data = list(reversed(data))

        self._data = data
        self.x_label = x if isinstance(x, str) else None
        self.y_label = y if isinstance(y, str) else None
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

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
        Add vertical bars on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx : Context
            Context
        """
        group = svg.append("g").attr("class", "bars")

        if self._opacity != 1.0:
            group.attr("opacity", self._opacity)
        if self._stroke_opacity != 1.0:
            group.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_dasharray is not None:
            group.attr("stroke-dasharray", self._stroke_dasharray)
        if self._fill_opacity != 1.0:
            group.attr("fill-opacity", self._fill_opacity)

        (
            group.select_all()
            .data(self._data)
            .join("rect")
            .attr("x", lambda d: ctx.x(self._x(d)))
            .attr("y", lambda d: ctx.y(self._y(d)))
            .attr("height", lambda d: ctx.y(0) - ctx.y(self._y(d)))
            .attr("width", ctx.x.get_bandwidth())
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
        )
