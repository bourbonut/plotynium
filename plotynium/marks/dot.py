from detroit.selection.selection import Selection
from collections.abc import Callable
from ..transformers import getter, Identity, Color, Symbol, Maker
from ..domain import domain

class Dot:
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        stroke: Callable | str | None = None,
        fill: Callable | str | None = None,
        r: Callable | float | None = None,
        symbol: Callable | float | None = None,
        stroke_width: float | int = 1,
    ):
        self._data = data
        self.x_label = None if callable(x) else str(x)
        self.y_label = None if callable(y) else str(y)
        self._x = getter(x or 0)
        self._y = getter(y or 1)

        self.x_domain = domain(data, self._x)
        self.y_domain = domain(data, self._y)
        self._stroke = Color.try_init(data, stroke, Identity(stroke or "black"))
        self._fill = Color.try_init(data, fill, Identity(fill or "none"))
        self._r = r if callable(r) else Identity(r or 3)
        self._symbol = Symbol.try_init(data, symbol)
        self._stroke_width = stroke_width

    def set_color_scheme(self, scheme):
        if scheme is None:
            return
        if isinstance(self._stroke, Maker):
            self._stroke.set_color_scheme(scheme)
        if isinstance(self._fill, Maker):
            self._fill.set_color_scheme(scheme)

    def __call__(
        self,
        svg: Selection,
        width: int,
        height: int,
        margin: tuple[int, int, int, int],
        x: Callable,
        y: Callable,
    ):

        if self._symbol is None:
            (
                svg.append("g")
                .select_all("circle")
                .data(self._data)
                .join("circle")
                .attr("transform", lambda d: f"translate({x(self._x(d))}, {y(self._y(d))})")
                .attr("stroke", self._stroke)
                .attr("fill", self._fill)
                .attr("stroke-width", self._stroke_width)
                .attr("r", self._r)
            )
        else:
            (
                svg.append("g")
                .select_all("circle")
                .data(self._data)
                .join("g")
                .attr("transform", lambda d: f"translate({x(self._x(d))}, {y(self._y(d))})")
                .append("path")
                .attr("d", self._symbol)
                .attr("stroke", self._stroke)
                .attr("fill", self._fill)
                .attr("stroke-width", self._stroke_width)
            )

