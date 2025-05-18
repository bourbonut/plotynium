from collections.abc import Callable
from operator import itemgetter

from ..types import Data, Index, T


def getter(
    value: str | Index | Callable[[T], Data],
) -> Callable[[Index], Data] | Callable[[str], Data] | Callable[[T], Data]:
    """
    Returns `value` if it is callable.
    Else it transforms `value` into a function `itemgetter`

    Parameters
    ----------
    value : str | Index | Callable[[T], Data]
        Key value, index or function for accessing value

    Returns
    -------
    Callable[[Index], Data] | Callable[[str], Data] | Callable[[T], Data]
        Accessor function
    """
    return value if callable(value) else itemgetter(value)
