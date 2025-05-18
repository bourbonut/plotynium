from typing import Callable

from ..types import Index, U, V
from .color import Color
from .constant import Constant
from .default import DefaultTransformer
from .getter import getter
from .identity import Identity
from .picker import LegendPicker
from .symbol import Symbol
from .transformer import Transformer

__all__ = [
    "Color",
    "Identity",
    "Constant",
    "DefaultTransformer",
    "Transformer",
    "Symbol",
    "LegendPicker",
    "init_transformer",
    "getter",
]


def init_transformer(
    transformer_class: type[Transformer[U, V]],
    data: list[U],
    value: str | Index | Callable[[U], V] | None = None,
    default: Transformer[U, V] | None = None,
) -> Transformer[U, V] | None:
    """
    This function intends to init a `Transformer` class given the type of `value` and
    how `data` are typed.

    Parameters
    ----------
    transformer_class : type[Transformer[U, V]]
        `Transformer` class
    data : list[T]
        Data used for the `Transformer` class.
    value : str | Index | Callable[[U], V] | None
        Key value or index or accessor function or undefined value
    default : Transformer[U, V] | None
        Default `Transformer` class (i.e. `Constant` or `Identity`)

    Returns
    -------
    Transformer[U, V] | None
        It could be directly `value` or a `Transformer` class from the given value.
    """
    if value is None or len(data) == 0:
        return default
    if callable(value):
        return DefaultTransformer(data, value)
    sample = data[0]
    is_str = isinstance(value, str) and value in sample
    is_index = isinstance(value, int) and value < len(sample)
    if is_str or is_index:
        return transformer_class(data, value)
    return default
