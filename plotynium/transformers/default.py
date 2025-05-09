from .transformer import Transformer
from ..types import U, V
from .picker import LegendPicker
from typing import Callable
from collections import OrderedDict

class DefaultTransformer(Transformer[U, V]):
    """
    When a specific function is indicated for `fill`, `stroke` or `symbol` arguments,
    this transformer helps to make `labels` thanks to `LegendPicker`.

    Parameters
    ----------
    data : list[U]
        Unused parameter
    value : Callable[[U], V]
        Function which takes a data and returns a value
    """
    def __init__(self, data: list[U], value: Callable[[U], V]):
        self._transform = value
        self._picker = LegendPicker()
 
    def __call__(self, d: U) -> V:
        """
        Transforms a data into a value by applying the `value` function.

        Parameters
        ----------
        d : U
            Data input

        Returns
        -------
        V
            Output of `value` function
        """
        return self._picker(self._transform(d))

    def get_mapping(self) -> OrderedDict[str, V]:
        """
        Returns the mapping of the picker.

        Returns
        -------
        OrderedDict[str, V]
            Ordered dictionary where keys are labels and values are generally
            colors.
        """
        return self._picker.get_mapping()
