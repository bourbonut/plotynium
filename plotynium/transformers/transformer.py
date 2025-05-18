from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

from ..types import ColorScheme, Index, U, V

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
    def __init__(self, data: list[U], value: str | Index | Callable[[U], V]): ...

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

    def set_color_scheme(self, scheme: ColorScheme):
        """
        Sets the color scheme if needed.

        Parameters
        ----------
        scheme : Interpolation | Scheme
            Parameter for color scheme
        """
        return

    def set_labels(self, labels: dict[int, str]):
        """
        Sets labels to the legend picker

        Parameters
        ----------
        labels : dict[int, str]
            Dictionary of labels where keys is the index of the label and
            values are each label
        """
        return

    def get_mapping(self) -> list[tuple[str, V]]:
        """
        Returns the mapping (label, value) of the transformation.

        Returns
        -------
        list[tuple[str, V]]
            List of pairs (labels, values) where values are generally colors.
        """
        return []
