from __future__ import annotations
from ..schemes import Scheme
from collections.abc import Callable
from abc import ABC, abstractmethod
from typing import Any

class Maker(ABC):

    @abstractmethod
    def __init__(self, data: list[Any], value: str):
        pass

    @abstractmethod
    def __call__(self, d: Any):
        pass

    def set_color_scheme(self, scheme: Scheme):
        return

    @staticmethod
    def try_init(data: list, value: str | Callable, default: Maker | None = None) -> Callable | None:
        pass
