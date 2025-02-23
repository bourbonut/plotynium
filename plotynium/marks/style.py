from collections.abc import Callable
from typing import Generic

from ..utils import getter, Constant, Color, Symbol
from ..schemes import Scheme
from ..interpolations import Interpolation
from ..options import ColorOptions
from ..types import T

import detroit as d3

class Style(Generic[T]):

    def __init__(
        self,
        data: list[T],
        default_stroke: str,
        default_fill: str,
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.,
        stroke_opacity: float = 1.,
        stroke_dasharray: str | None = None,
        opacity: float = 1.,
    ):
        self._fill = Color.try_init(data, fill, Constant(fill or default_fill))
        self._fill_opacity = fill_opacity

        self._stroke = Color.try_init(data, stroke, Constant(stroke or default_stroke))
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray
        self._stroke_opacity = stroke_opacity
        self._opacity = opacity
        self._scheme = ColorOptions().scheme

    @property
    def scheme(self) -> Interpolation | Scheme:
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: Interpolation | Scheme):
        self._fill.set_color_scheme(scheme)
        self._stroke.set_color_scheme(scheme)
        self._scheme = scheme
