from collections import OrderedDict

from ..types import T
from .picker import LegendPicker
from .transformer import Transformer


class Constant(Transformer[..., T]):
    """
    This class returns the same value constantly

    Parameters
    ----------
    value : T
        Value which will be returned by calling `__call__` method
    """

    def __init__(self, value: T):
        self._value = value
        self._picker = LegendPicker()

    def __call__(self, *args) -> T:
        """
        Returns the stored value

        Returns
        -------
        T
            Stored value by the class
        """
        return self._picker(self._value, self._value)

    def get_mapping(self) -> OrderedDict[str, T]:
        """
        Returns the mapping of the picker.

        Returns
        -------
        OrderedDict[str, T]
            Ordered dictionary where keys are labels and values are generally
            colors.
        """
        return self._picker.get_mapping()
