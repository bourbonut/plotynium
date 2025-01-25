from collections.abc import Callable
from operator import itemgetter

def getter(value: str | int | Callable):
    return value if callable(value) else itemgetter(value)
