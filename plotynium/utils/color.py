from ..options import ColorOptions
from ..schemes import Scheme
from ..interpolations import Interpolation
from ..types import Index, T, Data
from .getter import getter
from .maker import Maker
from typing import Any
from collections.abc import Callable
import detroit as d3

class Color(Maker[T, str]):
    def __init__(self, data: list, value: str | Index):
        self._value = getter(value)
        data = list(map(self._value, data))
        self._color = d3.scale_sequential([min(data), max(data)], ColorOptions().scheme)

    def __call__(self, d: T) -> str:
        d = self._value(d)
        return self._color(d)

    def set_color_scheme(self, scheme: Interpolation | Scheme):
        self._color.set_interpolator(scheme)

    @staticmethod
    def try_init(data: list[T], value: str | Index | Callable[[T], str], default: Maker[T, str] | None = None) -> Callable[[T], str] | None:
        return (
            value
            if callable(value)
            else (
                Color(data, value or default)
                if value is not None and value in data[0]
                else default
            )
        )
