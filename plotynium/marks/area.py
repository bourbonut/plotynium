from collections.abc import Callable
from detroit.selection import Selection

import detroit as d3

from .style import Style
from ..domain import domain, reduce
from ..scaler import determine_scaler, Scaler
from ..label import legend
from ..getter import getter
from ..transformers import Constant
from ..types import Data, Index, T

class AreaY(Style[T]):
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
        When incoherence found between 'y0' and 'y1' domains
    """
    def __init__(
        self,
        data: list[T],
        x: Callable[[T], Data] | Index | str | None = None,
        y: Callable[[T], Data] | Index | str | None = None,
        y1: Callable[[T], Data] | Index | str | None = None,
        y2: Callable[[T], Data] | Index | str | None = None,
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

        if y1 is not None and y2 is not None:
            self._y0 = getter(y1)
            self._y1 = getter(y2)
        elif y1 is None and y2 is None:
            self._y1 = getter(y or 1)
            self._y0 = Constant(0)
        else:
            raise ValueError("'y' must be specified or 'y1' and 'y2' must be specified.")

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
        Add an area defined by y values on SVG content.

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
        area = (
            d3.area()
            .x(
                (lambda d: x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINUOUS
                else (lambda d: x(self._x(d).timestamp()))
            )
            .y0(lambda d: y(self._y0(d)))
            .y1(lambda d: y(self._y1(d)))
        )

        (
            svg.append("g")
            .attr("class", "area")
            .append("path")
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
            .attr("d", area(self._data))
        )

