from collections.abc import Callable
from operator import itemgetter
from ..types import Data, Index, T


def getter(
    value: str | Index | Callable[[T], Data],
) -> Callable[[Index], Data] | Callable[[str], Data] | Callable[[T], Data]:
    return value if callable(value) else itemgetter(value)
