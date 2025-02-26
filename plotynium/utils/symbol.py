from ..types import Index, T, Data
from .getter import getter
from .maker import Maker
from collections.abc import Callable
import detroit as d3

class Symbol(Maker[T, str]):
    """
    This class makes an ordinal scaler which generates symbols based on data.

    Parameters
    ----------
    data : list[T]
        List of data
    value : str | Index | Callable[[T], Data]
        Index or key value for accessing data
    """
    def __init__(self, data: list[T], value: str | Index | Callable[[T], Data]):
        self._value = getter(value)
        self._labels = sorted(set(map(self._value, data)))
        self._symbol_type = d3.scale_ordinal(self._labels, d3.SYMBOLS_STROKE)

    def __call__(self, d: T) -> str:
        """
        Transforms a data into a symbol path

        Parameters
        ----------
        d : T
            Data input

        Returns
        -------
        str
            Symbol SVG path value
        """
        d = self._value(d)
        return d3.symbol(self._symbol_type(d))()

    @staticmethod
    def try_init(
        data: list[T],
        value: str | Index | Callable[[T], str] | None = None,
        default: Maker[T, str] | None = None,
    ) -> Callable[[T], str] | None:
        """
        If `values` is a callable, it returns it.
        Else it creates a `Symbol` depending on `value` type.

        Parameters
        ----------
        data : list[T]
            Data input used for `Symbol` if `value` is not callable
        value : str | Index | Callable[[T], str] | None
            Depending of the type, it is used for `Symbol` or directly returned by the
            function
        default : Maker[T, str] | None
            Default value used as second argument of `Symbol` if `value` is `None`

        Returns
        -------
        Callable[[T], str] | None
           `Symbol` if `value` is an index or a key value else it could be directly
           `value` when it is callable. If all arguments are `None` (except `data`),
           the function returns `None`.
        """
        if callable(value):
            return value
        elif (
            isinstance(value, str) and value in data[0]
        ) or (
            isinstance(value, int) and value < len(data[0])
        ):
            return Symbol(data, value)
        else:
            return default
