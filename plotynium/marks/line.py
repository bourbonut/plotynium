from collections.abc import Callable

import detroit as d3
from detroit.selection import Selection

from ..context import Context
from ..domain import domain
from ..scaler import Scaler, determine_scaler
from ..transformers import getter
from ..types import Data, T
from .mark import Mark
from .style import Style


class Line(Style[T], Mark):
    """
    Marker for drawing lines between point coordinates.

    Parameters
    ----------
    data : list[T]
        List where point coordinates are stored.
    x : Callable[[T], Data] | str | None
        X accessor function or key value
    y : Callable[[T], Data] | str | None
        Y accessor function or key value
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

        self.x_domain = domain(self._data, self._x)
        self.y_domain = domain(self._data, self._y)
        self.x_scaler_type = determine_scaler(self._data, self._x)
        self.y_scaler_type = determine_scaler(self._data, self._y)

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
        Adds lines from stored points on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        ctx : Context
            Context
        """
        self.set_colorscheme(ctx.color_scheme)
        self.set_labels(ctx.labels)
        line = (
            d3.line()
            .x(
                (lambda d: ctx.x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINUOUS
                else (lambda d: ctx.x(self._x(d).timestamp()))
            )
            .y(lambda d: ctx.y(self._y(d)))
        )

        group = svg.append("g").attr("class", "line")

        if self._opacity != 1.0:
            group.attr("opacity", self._opacity)
        if self._stroke_opacity != 1.0:
            group.attr("stroke-opacity", self._stroke_opacity)
        if self._stroke_dasharray is not None:
            group.attr("stroke-dasharray", self._stroke_dasharray)
        if self._fill_opacity != 1.0:
            group.attr("fill-opacity", self._fill_opacity)

        (
            group.select_all("path")
            .data(self.group())
            .enter()
            .append("path")
            .attr("fill", lambda d: d["fill"])
            .attr("stroke", lambda d: d["stroke"])
            .attr("stroke-width", self._stroke_width)
            .attr("d", lambda d: line(d["values"]))
        )
        ctx.update_color_mapping(
            self._stroke.get_mapping(),
            self._fill.get_mapping(),
        )

    def group(self) -> list[dict]:
        """
        Groups data according to their *stroke* and *fill* values.

        Returns
        -------
        list[dict]
            List of groups defined as dictionaries where:
            * the key `"stroke"` is the stroke value of the group
            * the key `"fill"` is the fill value of the group
            * the key `"values"` is a list of grouped data which has the same *stroke* and *fill* values
        """
        groups = {}
        for d in self._data:
            crits = {"stroke": self._stroke(d), "fill": self._fill(d)}
            _, values = groups.setdefault(tuple(crits.values()), (crits, []))
            values.append(d)
        return [crits | {"values": values} for crits, values in groups.values()]
