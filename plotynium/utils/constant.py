from .maker import Maker
from ..types import T
from typing import Generic

class Constant(Maker[..., T]):
    def __init__(self, value: T):
        self._value = value

    def __call__(self, *args) -> T:
        return self._value

