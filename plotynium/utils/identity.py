from .maker import Maker
from ..types import T
from typing import Generic

class Identity(Maker[T, T]):
    def __init__(self):
        pass

    def __call__(self, value: T) -> T:
        return value
