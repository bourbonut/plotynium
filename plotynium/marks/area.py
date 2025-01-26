from datetime import datetime
import detroit as d3
from detroit.selection.selection import Selection
from collections.abc import Callable
from ..transformers import getter, Identity, Color, Symbol, Maker
from ..domain import domain, reduce
from ..schemes import Scheme
from ..scaler import Scaler

class AreaY:
    def __init__(
        self,
        data: list,
        x: Callable | str | None = None,
        y: Callable | str | None = None,
        y1: Callable | str | None = None,
        y2: Callable | str | None = None,
        stroke: Callable | str | None = None,
        fill: Callable | str | None = None,
        stroke_width: float | int = 1,
    ):
        self._data = data
        self.x_label = None if callable(x) else str(x)
        self.y_label = None if callable(y) else str(y)
        self._x = getter(x or 0)
        if y is not None:
            self._y1 = getter(y or 1)
            self._y0 = Identity(0)
        elif y1 is not None or y2 is not None:
            self._y0 = getter(y1)
            self._y1 = getter(y2)
        else:
            raise ValueError("'y' must be specified or 'y1' and 'y2' must be specified.")

        self.x_domain, self.x_scaler_type = domain(data, self._x)
        y0_domain, y0_scaler_type = domain(data, self._y0)
        y1_domain, y1_scaler_type = domain(data, self._y1)
        if y0_scaler_type == y1_scaler_type:
            self.y_scaler_type = y0_scaler_type
        else:
            raise RuntimeError(
                "Incoherence between 'y0' and 'y1' domains "
                f"(found y0 domain: {y0_domain} and y1 domain : {y1_domain})"
            )
        self.y_domain = reduce([y0_domain, y1_domain])
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
        area = (
            d3.area()
            .x(
                (lambda d: x(self._x(d)))
                if self.x_scaler_type == Scaler.CONTINOUS
                else (lambda d: x(self._x(d).timestamp()))
            )
            .y0(lambda d: y(self._y0(d)))
            .y1(lambda d: y(self._y1(d)))
        )

        (
            svg.append("path")
            .attr("fill", self._fill)
            .attr("stroke", self._stroke)
            .attr("stroke-width", self._stroke_width)
            .attr("d", area(self._data))
        )

