from collections.abc import Callable
from operator import itemgetter
from typing import overload

from ..types import Data, T


@overload
def getter(value: str) -> itemgetter[str]: ...


@overload
def getter(value: int) -> itemgetter[int]: ...


@overload
def getter(value: Callable[[T], Data]) -> Callable[[T], Data]: ...


def getter(value):
    """
    Returns `value` if it is callable.
    Else it transforms `value` into a function `itemgetter`.

    Parameters
    ----------
    value : str | Callable[[T], Data]
        Key value, index or function for accessing value

    Returns
    -------
    Callable[[int], Data] | Callable[[str], Data] | Callable[[T], Data]
        Accessor function
    """
    return value if callable(value) else itemgetter(value)
