from .transformer import Transformer
from ..types import T
from typing import Generic

class Identity(Transformer[T, T]):
    """
    This class has only one method: `__call__`.
    This method returns the same value as the input.
    """
    def __init__(self):
        pass

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
