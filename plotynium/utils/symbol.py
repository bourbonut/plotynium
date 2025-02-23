from ..types import Index, T
from .getter import getter
from .maker import Maker
from collections.abc import Callable
import detroit as d3

class Symbol(Maker[T, str]):
    def __init__(self, data: list[T], value: str | Index):
        self._value = getter(value)
        self._labels = sorted(set(map(self._value, data)))
        self._symbol_type = d3.scale_ordinal(self._labels, d3.SYMBOLS_STROKE)

    def __call__(self, d: T) -> str:
        d = self._value(d)
        return d3.symbol(self._symbol_type(d))()

    @staticmethod
    def try_init(data: list[T], value: str | Index | Callable[[T], str], default: Maker[T, str] | None = None) -> Callable[[T], str] | None:
        return (
            value
            if callable(value)
            else (
                Symbol(data, value or default)
                if value is not None and value in data[0]
                else default
            )
        )
