from collections.abc import Callable
from detroit.selection.selection import Selection

import detroit as d3

from .style import Style
from ..domain import domain
from ..scaler import Scaler, determine_scaler
from ..utils import Identity, getter
from ..types import Data, T

class RuleY(Style[T]):
    """
    Marker for adding horizontal line given a list of y positions

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
        fill_opacity: float = 1.,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.5,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
        self._values = list(y)
        self._x = getter(0)
        self._y = getter(1)
        self.x_label = None
        self.y_label = None

        self.x_domain = None
        self.y_domain = [min(self._values), max(self._values)]
        self.x_scaler_type = None
        self.y_scaler_type = determine_scaler(self._values, Identity())
        self.legend_labels = None

        Style.__init__(
            self,
            data=[],
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
        Add horizontal lines on SVG content.

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
            .x(lambda d: x(self._x(d)))
            .y(
                (lambda d: y(self._y(d).timestamp()))
                if self.y_scaler_type == Scaler.TIME
                else lambda d: y(self._y(d))
            )
        )
        values = [[[x.domain[0], v], [x.domain[1], v]] for v in self._values]
        (
            svg.append("g")
            .attr("class", "rule")
            .select_all("rule")
            .data(values)
            .join("path")
            .attr("stroke", self._stroke)
            .attr("fill", self._fill)
            .attr("stroke-width", self._stroke_width)
            .attr("d", lambda d: line(d))
        )
