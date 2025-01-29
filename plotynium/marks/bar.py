from detroit.selection.selection import Selection
from collections.abc import Callable
from ..transformers import getter, Identity, Color, Symbol, Maker
from ..domain import domain
from ..schemes import Scheme
from ..options import SortOptions
from ..scaler import Scaler, determine_scaler

class BarY:
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        sort: SortOptions | None = None,
        stroke: Callable | str | None = None,
        fill: Callable | str | None = None,
        stroke_width: float | int = 1,
    ):
        if sort is not None:
            data = sorted(data, key=getter(sort.by))
            if sort.descending:
                data = list(reversed(data))
        self._data = data
        self.x_label = None if callable(x) else str(x)
        self.y_label = None if callable(y) else str(y)
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(data, self._x)
        self.y_domain = domain(data, self._y)
        self.x_scaler_type = determine_scaler(data, self._x)
        self.y_scaler_type = determine_scaler(data, self._y)
        self._stroke = Color.try_init(data, stroke, Identity(stroke or "none"))
        self._fill = Color.try_init(data, fill, Identity(fill or "black"))
        self._stroke_width = stroke_width

    def set_color_scheme(self, scheme: Scheme):
        if scheme is None:
            return
        if isinstance(self._stroke, Maker):
            self._stroke.set_color_scheme(scheme)
        if isinstance(self._fill, Maker):
            self._fill.set_color_scheme(scheme)

    def __call__(
        self,
        svg: Selection,
        x: Callable,
        y: Callable,
    ):
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
