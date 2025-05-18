from collections.abc import Callable

import detroit as d3

from ..types import Index, T
from .default import DefaultTransformer
from .getter import getter
from .identity import Identity
from .picker import LegendPicker
from .transformer import Transformer


class Symbol(Transformer[T, str]):
    """
    This class makes an ordinal scaler which generates symbols based on data.

    Parameters
    ----------
    data : list[T]
        List of data
    value : str | Index
        Index or key value for accessing data
    """

    def __init__(self, data: list[T], value: str | Index):
        self._value = getter(value)
        self._labels = sorted(set(map(self._value, data)))
        self._symbol_type = d3.scale_ordinal(self._labels, d3.SYMBOLS_STROKE)
        self._picker = LegendPicker()

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
        value = self._value(d)
        symbol = d3.symbol(self._symbol_type(value))()
        return self._picker(value, symbol)

    def set_labels(self, labels: dict[int, str]):
        """
        Sets labels to the legend picker

        Parameters
        ----------
        labels : dict[int, str]
            Dictionary of labels where keys is the index of the label and
            values are each label
        """
        self._picker = LegendPicker(labels)

    def get_mapping(self) -> list[tuple[str, str]]:
        """
        Returns the mapping of the picker.

        Returns
        -------
        list[tuple[str, str]]
            List of pairs (labels, colors).
        """
        return self._picker.get_mapping()

    @staticmethod
    def try_init(
        data: list[T],
        value: str | Index | Callable[[T], str] | None = None,
        default: Transformer[T, str] | None = None,
    ) -> Transformer[T, str] | None:
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
        default : Transformer[T, str] | None
            Default value used as second argument of `Symbol` if `value` is `None`

        Returns
        -------
        Transformer[T, str] | None
           `Symbol` if `value` is an index or a key value else it could be directly
           `value` when it is callable. If all arguments are `None` (except `data`),
           the function returns `None`.
        """
        if callable(value):
            return DefaultTransformer(data, value)
        elif len(data) > 0 and (
            (isinstance(value, str) and value in data[0])
            or (isinstance(value, int) and value < len(data[0]))
        ):
            return Symbol(data, value)
        else:
            return Identity() if default is None else default
