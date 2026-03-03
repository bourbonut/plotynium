from __future__ import annotations

from collections.abc import Hashable, Iterable
from enum import Enum, auto
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


class UniqueVariant(Enum):
    UNIQUE_VALUE = auto()
    NO_VALUE = auto()
    MULTIPLE_VALUES = auto()


def unique(values: Iterable[T]) -> tuple[T | list[T] | None, UniqueVariant]:
    values_set = set(values) - {None}
    if len(values_set) > 1:
        return list(values_set), UniqueVariant.MULTIPLE_VALUES
    elif len(values_set) == 0:
        return None, UniqueVariant.NO_VALUE
    return values_set.pop(), UniqueVariant.UNIQUE_VALUE


def unique_str(strings: list[str | None]) -> str | None:
    """
    Reduces a list of strings into an unique one by checking consistency between
    strings. For instance, if there are different strings, the function will
    return `None`. However, if only the same label in the given list was found,
    it is returned by the function.

    Parameters
    ----------
    strings : list[str | None]
        List of strings

    Returns
    -------
    str | None
        Unique string from the given list or undefined string as `None`
    """
    unique_strings = set(strings) - {None}
    if len(unique_strings) == 1:
        if string := unique_strings.pop():
            return string
