from collections.abc import Callable
from operator import itemgetter

import detroit as d3
from detroit.selection.selection import Selection

def getter(value):
    return value if callable(value) else itemgetter(value)

def identity(value):
    def local(*args):
        return value
    return local

class ColorMaker:
    def __init__(self, data: list, value: str):
        self._value = getter(value)
        data = list(map(self._value, data))
        self._color = d3.scale_sequential([min(data), max(data)], d3.interpolate_turbo)

    def __call__(self, d):
        d = self._value(d)
        return self._color(d)

    def set_color_scheme(self, scheme):
        self._color.set_interpolator(scheme)

class SymbolMaker:
    def __init__(self, data: list, value: str):
        self._value = getter(value)
        data = list(set(map(self._value, data)))
        self._symbol_type = d3.scale_ordinal(data, d3.SYMBOLS_STROKE)

    def __call__(self, d):
        d = self._value(d)
        return d3.symbol(self._symbol_type(d))()

def domain(data, accessor):
    values = list(map(accessor, data))
    return [min(values), max(values)]

def attr(maker, data: list, value: str, default: Callable | None = None):
    return (
        value
        if callable(value)
        else (
            maker(data, value or default)
            if value is not None and value in data[0]
            else default
        )
    )


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
        self._stroke = attr(ColorMaker, data, stroke, identity(stroke or "black"))
        self._fill = attr(ColorMaker, data, fill, identity(fill or "none"))
        self._r = r if callable(r) else identity(r or 3)
        self._symbol = attr(SymbolMaker, data, symbol, None)
        self._stroke_width = stroke_width

    def set_color_scheme(self, scheme):
        if scheme is None:
            return
        if isinstance(self._stroke, ColorMaker):
            self._stroke.set_color_scheme(scheme)
        if isinstance(self._fill, ColorMaker):
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
