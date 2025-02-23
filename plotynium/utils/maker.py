from ..schemes import Scheme
from ..interpolations import Interpolation
from ..types import Index, U, V
from collections.abc import Callable
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TMaker = TypeVar("TMaker", bound="Maker")

class Maker(Generic[U, V], ABC):

    @abstractmethod
    def __init__(self, data: list[U], value: str | Index):
        pass

    @abstractmethod
    def __call__(self, d: U) -> V:
        pass

    def set_color_scheme(self, scheme: Interpolation | Scheme):
        return

    @staticmethod
    def try_init(data: list[U], value: str | Index | Callable[[U], V], default: TMaker | None = None) -> Callable[[U], V] | None:
        pass
