from ..schemes import Scheme
from ..interpolations import Interpolation
from ..types import Index, U, V
from collections.abc import Callable
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TTransformer = TypeVar("TTransformer", bound="Transformer")

class Transformer(Generic[U, V], ABC):
    """
    Abstract class which defines the list of methods needed for a `Transformer`.

    Parameters
    ----------
    data : list[U]
        List of data
    value : str | Index | Callable[[U], V]
        Key value or index or accessor function
    """

    @abstractmethod
    def __init__(self, data: list[U], value: str | Index | Callable[[U], V]):
        ...

    @abstractmethod
    def __call__(self, d: U) -> V:
        """
        Transforms the data into a new type.

        Parameters
        ----------
        d : U
            Data input

        Returns
        -------
        V
            Transformed data
        """
        ...

    def set_color_scheme(self, scheme: Interpolation | Scheme):
        """
        Sets the color scheme if needed.

        Parameters
        ----------
        scheme : Interpolation | Scheme
            Parameter for color scheme
        """
        return NotImplementedError("This method is not implemented for this class.")
