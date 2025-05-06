from collections.abc import Callable
from detroit.selection import Selection

import detroit as d3

from .style import Style
from ..domain import domain
from ..label import legend
from ..scaler import Scaler, determine_scaler
from ..getter import getter
from ..types import Data, T

class Line(Style[T]):
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
        fill_opacity: float = 1.,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
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

        makers = (self._stroke, self._fill)
        self.legend_labels = legend(
            [
                maker.labels for maker in makers
                if hasattr(maker, "labels")
            ]
        )

    def __call__(
        self,
        svg: Selection,
        x: Callable,
        y: Callable,
        **kwargs,
    ):
        """
        Add lines from stored points on SVG content.

        Parameters
        ----------
        svg : Selection
            SVG Content
        x : Callable
            X scaler from `plot` function
        y : Callable
            Y scaler from `plot` function
        **kwargs
            Additional keyword arguments not used
        """
        line = (
            d3.line()
            .x(
                (lambda d: x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINUOUS
                else (lambda d: x(self._x(d).timestamp()))
            )
            .y(lambda d: y(self._y(d)))
        )

        (
            svg.append("g")
            .attr("class", "line")
            .select_all("path")
            .data(self.group())
            .enter()
            .append("path")
            .attr("fill", lambda d: d["fill"])
            .attr("stroke", lambda d: d["stroke"])
            .attr("stroke-width", self._stroke_width)
            .attr("d", lambda d: line(d["values"]))
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
