from collections.abc import Callable
from detroit.selection import Selection

from .style import Style
from ..options import SortOptions, init_options
from ..getter import getter
from ..label import legend
from ..domain import domain
from ..scaler import determine_scaler
from ..types import T, Data

class BarY(Style[T]):
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
        fill_opacity: float = 1.,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
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
        Add vertical bars on SVG content.

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
        (
            svg.append("g")
            .attr("class", "bars")
            .select_all()
            .data(self._data)
            .join("rect")
            .attr("x", lambda d: x(self._x(d)))
            .attr("y", lambda d: y(self._y(d)))
            .attr("height", lambda d: y(0) - y(self._y(d)))
            .attr("width", x.bandwidth)
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
        )
