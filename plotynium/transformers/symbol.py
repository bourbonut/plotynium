from .getter import getter
from .maker import Maker
from collections.abc import Callable
import detroit as d3

class Symbol(Maker):
    def __init__(self, data: list, value: str):
        self._value = getter(value)
        data = list(set(map(self._value, data)))
        self._symbol_type = d3.scale_ordinal(data, d3.SYMBOLS_STROKE)

    def __call__(self, d):
        d = self._value(d)
        return d3.symbol(self._symbol_type(d))()

    @staticmethod
    def try_init(data: list, value: str | Callable, default: Maker | None = None) -> Callable | None:
        return (
            value
            if callable(value)
            else (
                Symbol(data, value or default)
                if value is not None and value in data[0]
                else default
            )
        )
