from .transformer import Transformer
from ..types import T
from .picker import LegendPicker
from collections import OrderedDict

class Identity(Transformer[T, T]):
    """
    This class has only one method: `__call__`.
    This method returns the same value as the input.
    """
    def __init__(self):
        self._picker = LegendPicker()

    def __call__(self, value: T) -> T:
        """
        Returns the same value as the input.

        Parameters
        ----------
        value : T
            Input value

        Returns
        -------
        T
            Same value as input
        """
        return value

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
