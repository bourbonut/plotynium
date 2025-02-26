from ..schemes import Scheme
from ..interpolations import Interpolation
from ..types import Index, U, V
from collections.abc import Callable
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TMaker = TypeVar("TMaker", bound="Maker")

class Maker(Generic[U, V], ABC):
    """
    Abstract class which defines the list of methods needed for a `Maker`.

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
        default: TMaker | None = None,
    ) -> Callable[[U], V] | None:
        """
        This method intends to make a `Maker` class when it is possible.

        Parameters
        ----------
        data : list[T]
            Data used for the `Maker` class.
        value : str | Index | Callable[[T], str] | None
            Key value or index or accessor function or undefined value
        default : TMaker[T, str] | None
            Default `Maker` class (i.e. `Constant` or `Identity`)

        Returns
        -------
        Callable[[T], str] | None
            It could be directly `value` or a `Maker` class from the given value.
        """
        return NotImplementedError("This method is not implemented for this class.")
