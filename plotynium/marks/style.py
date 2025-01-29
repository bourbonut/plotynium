from collections.abc import Callable

from ..transformers import getter, Identity, Color, Symbol
from ..schemes import Scheme

import detroit as d3

class Style:

    def __init__(
        self,
        data: list,
        default_stroke: str,
        default_fill: str,
        fill: Callable | str | None = None,
        fill_opacity: float = 1.,
        stroke: Callable | str | None = None,
        stroke_width: float = 1.,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
        self._fill = Color.try_init(data, fill, Identity(fill or default_fill))
        self._fill_opacity = fill_opacity

        self._stroke = Color.try_init(data, stroke, Identity(stroke or default_stroke))
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray
        self._stroke_opacity = stroke_opacity
        self._opacity = opacity
        self._scheme = d3.interpolate_turbo

    @property
    def scheme(self) -> Scheme:
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: Scheme):
        self._fill.set_color_scheme(scheme)
        self._stroke.set_color_scheme(scheme)
