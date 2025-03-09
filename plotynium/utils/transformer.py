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

    @staticmethod
    def try_init(
        data: list[U],
        value: str | Index | Callable[[U], V] | None = None,
        default: TTransformer | None = None,
    ) -> Callable[[U], V] | None:
        """
        This method intends to make a `Transformer` class when it is possible.

        Parameters
        ----------
        data : list[T]
            Data used for the `Transformer` class.
        value : str | Index | Callable[[T], str] | None
            Key value or index or accessor function or undefined value
        default : TTransformer[T, str] | None
            Default `Transformer` class (i.e. `Constant` or `Identity`)

        Returns
        -------
        Callable[[T], str] | None
            It could be directly `value` or a `Transformer` class from the given value.
        """
        return NotImplementedError("This method is not implemented for this class.")
