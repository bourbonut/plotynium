from .transformer import Transformer
from ..types import T
from typing import Generic

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

    def __call__(self, *args) -> T:
        """
        Returns the stored value

        Returns
        -------
        T
            Stored value by the class
        """
        return self._value

