from collections.abc import Callable
from operator import itemgetter
from typing import overload

from ..types import Data, T


@overload
def getter(value: None) -> None: ...


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
    value : int | str | Callable[[T], Data]
        Key value, index or function for accessing value

    Returns
    -------
    itemgetter[int] | itemgetter[str]| Callable[[T], Data] | None
        Accessor function
    """
    if value is None:
        return None
    elif callable(value):
        return value
    else:
        return itemgetter(value)
